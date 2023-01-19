import typer

from sirtuin.controllers.aws_beanstalk import (
    create_beanstalk_from_config,
    deploy_beanstalk_from_config,
    terminate_beanstalk_from_config,
    upgrade_beanstalk_from_config,
)
from sirtuin.controllers.aws_cloudfront import (
    deploy_cloudfront_from_config,
    invalidate_cloudfront_from_config,
)
from sirtuin.controllers.aws_compute import create_load_balancer_from_prompt
from sirtuin.controllers.aws_container import (
    deploy_container_from_config,
    push_container_from_config,
)
from sirtuin.controllers.http_headers import print_content_security_policy
from sirtuin.utils.constants import DEFAULT_SIRTUIN_CONFIG_NAME

cli = typer.Typer()

# ? Elastic Compute


@cli.command()
def compute_create_lb(
    load_balancer_name: str = typer.Option(..., prompt="Choose Load Balancer Name"),
    load_balancer_type: str = typer.Option(..., prompt="Choose Load Balancer Type"),
    load_balancer_subnets: str = typer.Option(..., prompt="Choose Subnets"),
    aws_region: str = typer.Option(..., prompt="Choose AWS Region"),
    aws_profile: str = typer.Option(..., prompt="Choose AWS Profile"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    create_load_balancer_from_prompt(
        load_balancer_name,
        load_balancer_type,
        load_balancer_subnets,
        aws_region,
        aws_profile,
        verbose=verbose,
    )


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


# ? Elastic Beanstalk


@cli.command()
def beanstalk_create(
    filepath: str = typer.Argument(default=DEFAULT_SIRTUIN_CONFIG_NAME),
    profile: str = typer.Option("default", "--profile", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    create_beanstalk_from_config(filepath, profile, verbose)


@cli.command()
def beanstalk_upgrade(
    filepath: str = typer.Argument(default=DEFAULT_SIRTUIN_CONFIG_NAME),
    profile: str = typer.Option("default", "--profile", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    upgrade_beanstalk_from_config(filepath, profile, verbose)


@cli.command()
def beanstalk_deploy(
    filepath: str = typer.Argument(default=DEFAULT_SIRTUIN_CONFIG_NAME),
    profile: str = typer.Option("default", "--profile", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    deploy_beanstalk_from_config(filepath, profile, verbose)


@cli.command()
def beanstalk_terminate(
    filepath: str = typer.Argument(default=DEFAULT_SIRTUIN_CONFIG_NAME),
    profile: str = typer.Option("default", "--profile", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    terminate_beanstalk_from_config(filepath, profile, verbose)


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
