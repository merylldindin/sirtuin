import os
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
from sirtuin.utils.decorators import run_command
from sirtuin.utils.dumpers import copy_file, dump_as_json, dump_as_raw, dump_as_yaml
from sirtuin.utils.filepaths import get_schemas_path, get_service_directory
from sirtuin.utils.loaders import read_dotenv_file, read_raw_file, read_toml_file


def _get_sirtuin_config(filepath: str) -> ElasticBeanstalkSirtuinConfig:
    config = ElasticBeanstalkSirtuinConfig(**read_toml_file(filepath))
    config.directory = get_service_directory()

    return config


def _get_environment_variables(
    config: ElasticBeanstalkSirtuinConfig,
) -> dict[str, str] | None:
    if config.beanstalk.dotenv_path is None:
        return None

    return read_dotenv_file(
        os.path.join(config.directory, config.beanstalk.dotenv_path)
    )


def _write_ebignore_config(config: ElasticBeanstalkSirtuinConfig) -> str:
    filepath = os.path.join(config.directory, DEFAULT_BEANSTALK_EBIGNORE_PATH)

    dump_as_raw("*\n\n!artifact.zip", filepath)

    return filepath


def _write_beanstalk_config(config: ElasticBeanstalkSirtuinConfig) -> str:
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

    filepath = os.path.join(config.directory, DEFAULT_BEANSTALK_CONFIG_PATH)

    dump_as_yaml(beanstalk_config.dict(by_alias=True), filepath)

    return filepath


def _write_dockerrun_config(config: ElasticBeanstalkSirtuinConfig) -> str:
    dockerrun_config = ElasticBeanstalkDockerrunConfig(
        **{
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
            "Authentication": {
                "Bucket": config.docker.auth_bucket,
                "Key": config.docker.auth_key,
            },
        }
    )

    filepath = os.path.join(config.directory, DEFAULT_BEANSTALK_DOCKERRUN_PATH)

    dump_as_json(dockerrun_config.dict(by_alias=True, use_sanitization=True), filepath)

    return filepath


def _inject_variables(filepath: str, variables: dict[str, str | int]) -> None:
    source = read_raw_file(filepath)

    for variable, value in variables.items():
        source = source.replace(f"$_{variable}_$", str(value))

    dump_as_raw(source, filepath)


def _write_extensions(
    files: dict[str, dict[str, str | int] | None],
    schema_source: str,
    target_directory: str,
    known_extensions: list[str],
) -> None:
    for file, variables in files.items():
        filepath = os.path.join(target_directory, file)

        copy_file(os.path.join(schema_source, file), filepath)

        if variables is not None:
            _inject_variables(filepath, variables)

        known_extensions.append(filepath)


def _write_beanstalk_customization(config: ElasticBeanstalkSirtuinConfig) -> list[str]:
    extensions: list[str] = []

    _write_extensions(
        config.ebextensions,
        os.path.join(get_schemas_path(), DEFAULT_BEANSTALK_EBEXTENSIONS_SCHEMAS),
        os.path.join(config.directory, DEFAULT_BEANSTALK_EBEXTENSIONS_DIRECTORY),
        extensions,
    )

    _write_extensions(
        config.platform,
        os.path.join(get_schemas_path(), DEFAULT_BEANSTALK_PLATFORM_SCHEMAS),
        os.path.join(config.directory, DEFAULT_BEANSTALK_PLATFORM_DIRECTORY),
        extensions,
    )

    return extensions


def _setup_beanstalk_deployment(config: ElasticBeanstalkSirtuinConfig) -> str:
    _write_ebignore_config(config)

    _write_beanstalk_config(config)

    filepaths: list[str] = [
        _write_dockerrun_config(config),
        *_write_beanstalk_customization(config),
    ]

    artifact = os.path.join(config.directory, DEFAULT_BEANSTALK_ARTIFACT_PATH)

    with ZipFile(artifact, mode="w") as zip_file:
        for filepath in filepaths:
            if len(config.directory) > 0:
                zip_file.write(
                    filepath, arcname=filepath.replace(config.directory, ".")
                )
            else:
                zip_file.write(filepath)

    return artifact


def _clean_beanstalk_deployment(config: ElasticBeanstalkSirtuinConfig) -> None:
    delete_file(os.path.join(config.directory, DEFAULT_BEANSTALK_ARTIFACT_PATH))
    delete_file(os.path.join(config.directory, DEFAULT_BEANSTALK_DOCKERRUN_PATH))
    delete_file(os.path.join(config.directory, DEFAULT_BEANSTALK_EBIGNORE_PATH))

    delete_directory(os.path.join(config.directory, DEFAULT_BEANSTALK_CONFIG_DIRECTORY))
    delete_directory(
        os.path.join(config.directory, DEFAULT_BEANSTALK_EBEXTENSIONS_DIRECTORY)
    )
    delete_directory(
        os.path.join(config.directory, DEFAULT_BEANSTALK_PLATFORM_DIRECTORY)
    )


@run_command
def _create_beanstalk_service(config: ElasticBeanstalkSirtuinConfig) -> str:
    environment_variables = _get_environment_variables(config)
    if environment_variables is not None:
        environment_variables = ",".join(
            [f"{key}={value}" for key, value in environment_variables.items()]
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
        + (
            f"--envvars {environment_variables} "
            if environment_variables is not None
            else ""
        )
        + (
            (
                f"--shared-lb {config.load_balancer.shared_alb_name} "
                f"--shared-lb-port {config.load_balancer.shared_alb_port} "
            )
            if config.load_balancer.is_shared
            else ""
        )
        + f"--region {config.instance.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


def create_beanstalk_from_config(filepath: str) -> None:
    config = _get_sirtuin_config(filepath)

    _setup_beanstalk_deployment(config)
    _create_beanstalk_service(config)
    _clean_beanstalk_deployment(config)


@run_command
def _upgrade_beanstalk_instance(config: ElasticBeanstalkSirtuinConfig) -> str:
    return (
        f"eb upgrade {config.beanstalk.service} "
        f"--force "
        f"--region {config.instance.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


def upgrade_beanstalk_from_config(filepath: str) -> None:
    config = _get_sirtuin_config(filepath)

    _write_beanstalk_config(config)
    _upgrade_beanstalk_instance(filepath)
    _clean_beanstalk_deployment(config)


@run_command
def _deploy_beanstalk_service(config: ElasticBeanstalkSirtuinConfig) -> str:
    return (
        f"eb deploy {config.beanstalk.service} "
        f"--region {config.instance.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


def deploy_beanstalk_from_config(filepath: str) -> None:
    config = _get_sirtuin_config(filepath)

    _setup_beanstalk_deployment(config)
    _deploy_beanstalk_service(config)
    _clean_beanstalk_deployment(config)


@run_command
def _terminate_beanstalk_service(config: ElasticBeanstalkSirtuinConfig) -> str:
    return (
        f"eb terminate {config.beanstalk.service} "
        f"--force "
        f"--region {config.instance.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


def terminate_beanstalk_from_config(filepath: str) -> None:
    config = _get_sirtuin_config(filepath)

    _write_beanstalk_config(config)
    _terminate_beanstalk_service(config)
    _clean_beanstalk_deployment(config)
