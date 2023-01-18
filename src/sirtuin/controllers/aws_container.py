from pathlib import Path

from sirtuin.models.aws_container import ElasticContainerServiceConfig
from sirtuin.utils.constants import DEFAULT_AWS_PROFILE
from sirtuin.utils.decorators import catch_remote_config, run_command
from sirtuin.utils.loaders import read_toml_file


def _get_sirtuin_config(filepath: Path) -> ElasticContainerServiceConfig:
    return ElasticContainerServiceConfig(**read_toml_file(filepath))


@run_command(description="Connect to Elastic Container Registry")
def _login_registry(
    config: ElasticContainerServiceConfig, verbose: bool = False
) -> str:
    return (
        f"aws ecr get-login-password "
        f"--region {config.registry.region.value} "
        f"--profile {config.profile} "
        f"| docker login "
        f"--username AWS "
        f"--password-stdin {config.registry.account}"
    )


@run_command(description="Tag Container")
def _tag_container(config: ElasticContainerServiceConfig, verbose: bool = False) -> str:
    return (
        f"docker tag "
        f"{config.image.source} "
        f"{config.registry.account}/{config.image.target}"
    )


@run_command(description="Push Container to Elastic Container Registry")
def _push_container(
    config: ElasticContainerServiceConfig, verbose: bool = False
) -> str:
    return f"docker push {config.registry.account}/{config.image.target}"


@run_command(description="Untag Container")
def _untag_container(
    config: ElasticContainerServiceConfig, verbose: bool = False
) -> str:
    return f"docker rmi {config.registry.account}/{config.image.target}"


@catch_remote_config
def push_container_from_config(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    config = _get_sirtuin_config(filepath)

    _login_registry(config, verbose)
    _tag_container(config, verbose)
    _push_container(config, verbose)
    _untag_container(config, verbose)


@run_command(description="Deploy Container to Elastic Container Service")
def _deploy_container(
    config: ElasticContainerServiceConfig, verbose: bool = False
) -> str:
    return (
        f"aws ecs update-service "
        f"--cluster {config.cluster.name} "
        f"--service {config.cluster.service} "
        f"--force-new-deployment "
        f"--region {config.cluster.region.value} "
        f"--profile {config.profile}"
    )


@catch_remote_config
def deploy_container_from_config(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    config = _get_sirtuin_config(filepath)

    _deploy_container(config, verbose)
