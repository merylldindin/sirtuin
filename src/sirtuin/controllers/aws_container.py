from pathlib import Path

from sirtuin.models.aws_container import ElasticContainerServiceConfig
from sirtuin.utils.constants import DEFAULT_AWS_PROFILE
from sirtuin.utils.decorators import catch_remote_config, run_command
from sirtuin.utils.loaders import read_toml_file


def _get_sirtuin_config(filepath: Path) -> ElasticContainerServiceConfig:
    return ElasticContainerServiceConfig(**read_toml_file(filepath))


@run_command(description="Connected to Elastic Container Registry")
def _login_container_registry(
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


@run_command(description="Tag Docker image")
def _tag_docker_image(
    config: ElasticContainerServiceConfig, verbose: bool = False
) -> str:
    return (
        f"docker tag "
        f"{config.image.source} "
        f"{config.registry.account}/{config.image.target}"
    )


@run_command(description="Push Docker image to Elastic Container Registry")
def _push_docker_image(
    config: ElasticContainerServiceConfig, verbose: bool = False
) -> str:
    return f"docker push {config.registry.account}/{config.image.target}"


@run_command(description="Untag Docker image")
def _untag_docker_image(
    config: ElasticContainerServiceConfig, verbose: bool = False
) -> str:
    return f"docker rmi {config.registry.account}/{config.image.target}"


@catch_remote_config
def publish_docker_image_from_config(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    config = _get_sirtuin_config(filepath)

    _login_container_registry(config, verbose)
    _tag_docker_image(config, verbose)
    _push_docker_image(config, verbose)
    _untag_docker_image(config, verbose)
