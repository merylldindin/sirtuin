from pathlib import Path
from zipfile import ZipFile

from sirtuin.models.aws_beanstalk import (
    DEFAULT_BEANSTALK_ARTIFACT_PATH,
    DEFAULT_BEANSTALK_CONFIG_DIRECTORY,
    DEFAULT_BEANSTALK_CONFIG_PATH,
    DEFAULT_BEANSTALK_DOCKERRUN_PATH,
    DEFAULT_BEANSTALK_EBEXTENSIONS_DIRECTORY,
    DEFAULT_BEANSTALK_EBEXTENSIONS_SCHEMAS,
    DEFAULT_BEANSTALK_EBIGNORE_PATH,
    DEFAULT_BEANSTALK_PLATFORM_DIRECTORY,
    DEFAULT_BEANSTALK_PLATFORM_SCHEMAS,
    ElasticBeanstalkConfig,
    ElasticBeanstalkDockerrunConfig,
    ElasticBeanstalkSirtuinConfig,
)
from sirtuin.utils.cleaners import delete_directory, delete_file
from sirtuin.utils.constants import DEFAULT_AWS_PROFILE, DEFAULT_ENV_FILENAME
from sirtuin.utils.decorators import (
    catch_remote_config,
    run_command,
    run_interactive_subprocess,
)
from sirtuin.utils.dumpers import copy_file, dump_as_json, dump_as_raw, dump_as_yaml
from sirtuin.utils.filepaths import get_schemas_path
from sirtuin.utils.loaders import read_dotenv_file, read_raw_file, read_toml_file


def _get_sirtuin_config(
    filepath: Path, profile: str = "default"
) -> ElasticBeanstalkSirtuinConfig:
    raw_config = read_toml_file(filepath)

    if (
        dotenv_path := raw_config["beanstalk"].get("DotenvPath")
    ) is not None and dotenv_path.startswith("s3://"):
        run_interactive_subprocess(
            "Loading environment variables from S3",
            f"aws s3 cp {dotenv_path} {DEFAULT_ENV_FILENAME} --profile {profile}",
        )

        raw_config["beanstalk"]["DotenvPath"] = DEFAULT_ENV_FILENAME

    return ElasticBeanstalkSirtuinConfig(**raw_config)


def _get_environment_variables(
    config: ElasticBeanstalkSirtuinConfig,
) -> dict[str, str] | None:
    if config.beanstalk.dotenv_path is None:
        return None

    return read_dotenv_file(config.beanstalk.dotenv_path)


def _write_ebignore_config(_: ElasticBeanstalkSirtuinConfig) -> Path:
    dump_as_raw("*\n\n!artifact.zip", DEFAULT_BEANSTALK_EBIGNORE_PATH)

    return DEFAULT_BEANSTALK_EBIGNORE_PATH


def _write_beanstalk_config(config: ElasticBeanstalkSirtuinConfig) -> Path:
    beanstalk_config = ElasticBeanstalkConfig(
        **{
            "branch-defaults": {
                "default": {
                    "environment": config.beanstalk.service,
                }
            },
            "global": {
                "application_name": config.beanstalk.application,
                "default_ec2_keyname": config.beanstalk.ec2_keyname,
                "default_region": config.instance.region.value,
                "profile": config.profile,
            },
        }
    )

    dump_as_yaml(beanstalk_config.dict(by_alias=True), DEFAULT_BEANSTALK_CONFIG_PATH)

    return DEFAULT_BEANSTALK_CONFIG_PATH


def _write_dockerrun_config(config: ElasticBeanstalkSirtuinConfig) -> Path:
    raw_config = {
        "Image": {
            "Name": config.docker.image,
        },
        "Ports": [
            {"ContainerPort": port.container, "HostPort": port.host}
            for port in config.docker.ports
        ],
        "Volumes": [
            {"ContainerDirectory": volume.container, "HostDirectory": volume.host}
            for volume in config.docker.volumes
        ],
    }

    if config.docker.auth_key is not None and config.docker.auth_bucket is not None:
        raw_config["Authentication"] = {
            "Bucket": config.docker.auth_bucket,
            "Key": config.docker.auth_key,
        }

    dockerrun_config = ElasticBeanstalkDockerrunConfig(**raw_config)

    dump_as_json(
        dockerrun_config.dict(by_alias=True, exclude_none=True, use_sanitization=True),
        DEFAULT_BEANSTALK_DOCKERRUN_PATH,
    )

    return DEFAULT_BEANSTALK_DOCKERRUN_PATH


def _inject_variables(filepath: Path, variables: dict[str, str | int]) -> None:
    source = read_raw_file(filepath)

    for variable, value in variables.items():
        source = source.replace(f"$_{variable}_$", str(value))

    dump_as_raw(source, filepath)


def _write_extensions(
    files: dict[str, dict[str, str | int] | None],
    schema_source: Path,
    target_directory: Path,
    known_extensions: list[Path],
) -> None:
    for file, variables in files.items():
        copy_file(schema_source / file, target_directory / file)

        if variables is not None:
            _inject_variables(target_directory / file, variables)

        known_extensions.append(target_directory / file)


def _write_beanstalk_customization(config: ElasticBeanstalkSirtuinConfig) -> list[Path]:
    extensions: list[Path] = []

    _write_extensions(
        config.ebextensions,
        get_schemas_path() / DEFAULT_BEANSTALK_EBEXTENSIONS_SCHEMAS,
        DEFAULT_BEANSTALK_EBEXTENSIONS_DIRECTORY,
        extensions,
    )

    _write_extensions(
        config.platform,
        get_schemas_path() / DEFAULT_BEANSTALK_PLATFORM_SCHEMAS,
        DEFAULT_BEANSTALK_PLATFORM_DIRECTORY,
        extensions,
    )

    return extensions


def _setup_beanstalk_deployment(config: ElasticBeanstalkSirtuinConfig) -> Path:
    _write_ebignore_config(config)

    _write_beanstalk_config(config)

    filepaths: list[Path] = [
        _write_dockerrun_config(config)
    ] + _write_beanstalk_customization(config)

    with ZipFile(DEFAULT_BEANSTALK_ARTIFACT_PATH, mode="w") as zip_file:
        for filepath in filepaths:
            zip_file.write(filepath)

    return DEFAULT_BEANSTALK_ARTIFACT_PATH


def _clean_beanstalk_deployment(_: ElasticBeanstalkSirtuinConfig) -> None:
    for filepath in [
        Path(DEFAULT_ENV_FILENAME),
        DEFAULT_BEANSTALK_ARTIFACT_PATH,
        DEFAULT_BEANSTALK_DOCKERRUN_PATH,
        DEFAULT_BEANSTALK_EBIGNORE_PATH,
    ]:
        delete_file(filepath)

    for directory in [
        DEFAULT_BEANSTALK_CONFIG_DIRECTORY,
        DEFAULT_BEANSTALK_EBEXTENSIONS_DIRECTORY,
        DEFAULT_BEANSTALK_PLATFORM_DIRECTORY,
    ]:
        delete_directory(directory)


@run_command(description="Create Elastic Beanstalk application")
def _create_beanstalk_service(
    config: ElasticBeanstalkSirtuinConfig, verbose: bool = False
) -> str:
    environment_variables = _get_environment_variables(config)

    dumped_variables = (
        ",".join([f"{key}={value}" for key, value in environment_variables.items()])
        if environment_variables is not None
        else None
    )

    return (
        f"eb create {config.beanstalk.service} "
        f"--instance_type {config.instance.instance_type.value} "
        f"--min-instances {config.instance.min_instances} "
        f"--max-instances {config.instance.max_instances} "
        f"--elb-type {config.load_balancer.elb_type} "
        f"--timeout {config.instance.timeout} "
        f"--vpc.id {config.vpc.vpc_id} --vpc.elbpublic "
        f"--vpc.ec2subnets {config.vpc.ec2_subnets} "
        f"--vpc.dbsubnets {config.vpc.db_subnets} "
        f"--vpc.elbsubnets {config.vpc.elb_subnets} "
        + (f"--envvars {dumped_variables} " if dumped_variables is not None else "")
        + (
            (
                f"--shared-lb {config.load_balancer.shared_elb_name} "
                f"--shared-lb-port {config.load_balancer.shared_elb_port} "
            )
            if config.load_balancer.is_shared
            else ""
        )
        + f"--region {config.instance.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


@catch_remote_config
def create_beanstalk_from_config(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    config = _get_sirtuin_config(filepath, profile=profile)

    _setup_beanstalk_deployment(config)
    _create_beanstalk_service(config, verbose)
    _clean_beanstalk_deployment(config)


@run_command(description="Upgrade Elastic Beanstalk instance")
def _upgrade_beanstalk_instance(
    config: ElasticBeanstalkSirtuinConfig, verbose: bool = False
) -> str:
    return (
        f"eb upgrade {config.beanstalk.service} "
        f"--force "
        f"--region {config.instance.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


@catch_remote_config
def upgrade_beanstalk_from_config(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    config = _get_sirtuin_config(filepath, profile=profile)

    _write_beanstalk_config(config)
    _upgrade_beanstalk_instance(config, verbose)
    _clean_beanstalk_deployment(config)


@run_command(description="Deploy Elastic Beanstalk application")
def _deploy_beanstalk_service(
    config: ElasticBeanstalkSirtuinConfig, verbose: bool = False
) -> str:
    return (
        f"eb deploy {config.beanstalk.service} "
        f"--region {config.instance.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


@catch_remote_config
def deploy_beanstalk_from_config(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    config = _get_sirtuin_config(filepath, profile=profile)

    _setup_beanstalk_deployment(config)
    _deploy_beanstalk_service(config, verbose)
    _clean_beanstalk_deployment(config)


@run_command(description="Terminate Elastic Beanstalk instance")
def _terminate_beanstalk_service(
    config: ElasticBeanstalkSirtuinConfig, verbose: bool = False
) -> str:
    return (
        f"eb terminate {config.beanstalk.service} "
        f"--force "
        f"--region {config.instance.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


@catch_remote_config
def terminate_beanstalk_from_config(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    config = _get_sirtuin_config(filepath, profile=profile)

    _write_beanstalk_config(config)
    _terminate_beanstalk_service(config, verbose)
    _clean_beanstalk_deployment(config)
