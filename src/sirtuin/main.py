import typer

from sirtuin.controllers.aws_beanstalk import (
    create_beanstalk_from_config,
    deploy_beanstalk_from_config,
    terminate_beanstalk_service,
    upgrade_beanstalk_instance,
)
from sirtuin.controllers.aws_cloudfront import (
    deploy_cloudfront_from_config,
    invalidate_cloudfront_distribution,
)
from sirtuin.controllers.http_headers import print_content_security_policy
from sirtuin.models.routines import DEFAULT_CONFIG_FILE

cli = typer.Typer()


# ? HTTP Headers


@cli.command()
def generate_csp(
    filepath: str = typer.Argument(default=DEFAULT_CONFIG_FILE),
) -> None:
    print_content_security_policy(filepath)


# ? Elastic Beanstalk


@cli.command()
def create_beanstalk(
    filepath: str = typer.Argument(default=DEFAULT_CONFIG_FILE),
) -> None:
    create_beanstalk_from_config(filepath)


@cli.command()
def upgrade_beanstalk(
    filepath: str = typer.Argument(default=DEFAULT_CONFIG_FILE),
) -> None:
    upgrade_beanstalk_instance(filepath)


@cli.command()
def deploy_beanstalk(
    filepath: str = typer.Argument(default=DEFAULT_CONFIG_FILE),
) -> None:
    deploy_beanstalk_from_config(filepath)


@cli.command()
def terminate_beanstalk(
    filepath: str = typer.Argument(default=DEFAULT_CONFIG_FILE),
) -> None:
    terminate_beanstalk_service(filepath)


# ? Cloudfront


@cli.command()
def deploy_cloudfront(
    filepath: str = typer.Argument(default=DEFAULT_CONFIG_FILE),
) -> None:
    deploy_cloudfront_from_config(filepath)


@cli.command()
def create_invalidation(
    filepath: str = typer.Argument(default=DEFAULT_CONFIG_FILE),
) -> None:
    invalidate_cloudfront_distribution(filepath)
