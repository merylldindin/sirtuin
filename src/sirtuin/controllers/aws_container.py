from pathlib import Path

from sirtuin.models.aws_container import ElasticContainerServiceConfig
from sirtuin.utils.decorators import run_command
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


def publish_docker_image_from_config(filepath: Path, verbose: bool = False) -> None:
    config = _get_sirtuin_config(filepath)

    _login_container_registry(config, verbose=verbose)
    _tag_docker_image(config, verbose=verbose)
    _push_docker_image(config, verbose=verbose)
    _untag_docker_image(config, verbose=verbose)


@run_command(description="Create Elastic Container Service cluster")
def _create_ecs_cluster(
    config: ElasticContainerServiceConfig, verbose: bool = False
) -> str:
    return f"""
        aws ecs create-cluster
        --cluster-name {config.cluster.name}
        --region {config.cluster.region.value}
        --profile {config.profile}
    """


# @run_command(description="Create Elastic Container Service task definition")
# def _create_ecs_task_definition(
#     config: ElasticContainerServiceConfig, verbose: bool = False
# ) -> str:
#     return f"""
#         aws ecs register-task-definition
#         --cli-input-json file://task_definition.json
#         --region {config.cluster.region}
#         --profile {config.profile}
#     """

# @run_command(description="Create Elastic Container Service service")
# def _create_ecs_service(
#     config: ElasticContainerServiceConfig, verbose: bool = False
# ) -> str:
#     return f"""
#         aws ecs create-service
#         --cli-input-json file://service.json
#         --region {config.cluster.region}
#         --profile {config.profile}
#     """
