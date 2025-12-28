import typer

from sirtuin.controllers.aws_cloudfront import (
    deploy_cloudfront_from_config,
    invalidate_cloudfront_from_config,
)
from sirtuin.controllers.aws_container import (
    deploy_container_from_config,
    push_container_from_config,
)
from sirtuin.controllers.http_headers import print_content_security_policy
from sirtuin.utils.constants import DEFAULT_SIRTUIN_CONFIG_NAME

cli = typer.Typer()

# ? Elastic Container


@cli.command()
def container_push(
    filepath: str = typer.Argument(default=DEFAULT_SIRTUIN_CONFIG_NAME),
    profile: str = typer.Option("default", "--profile", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    push_container_from_config(filepath, profile, verbose)


@cli.command()
def container_deploy(
    filepath: str = typer.Argument(default=DEFAULT_SIRTUIN_CONFIG_NAME),
    profile: str = typer.Option("default", "--profile", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    deploy_container_from_config(filepath, profile, verbose)


# ? Cloudfront


@cli.command()
def cloudfront_deploy(
    filepath: str = typer.Argument(default=DEFAULT_SIRTUIN_CONFIG_NAME),
    profile: str = typer.Option("default", "--profile", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    deploy_cloudfront_from_config(filepath, profile, verbose)


@cli.command()
def cloudfront_invalidate(
    filepath: str = typer.Argument(default=DEFAULT_SIRTUIN_CONFIG_NAME),
    profile: str = typer.Option("default", "--profile", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    invalidate_cloudfront_from_config(filepath, profile, verbose)


@cli.command()
def cloudfront_headers(
    filepath: str = typer.Argument(default=DEFAULT_SIRTUIN_CONFIG_NAME),
    profile: str = typer.Option("default", "--profile", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    print_content_security_policy(filepath, profile, verbose)
