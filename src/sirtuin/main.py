from pathlib import Path

import typer

from sirtuin.controllers.aws_beanstalk import (
    create_beanstalk_from_config,
    deploy_beanstalk_from_config,
    terminate_beanstalk_from_config,
    upgrade_beanstalk_from_config,
)
from sirtuin.controllers.aws_cloudfront import (
    deploy_cloudfront_from_config,
    invalidate_cloudfront_distribution,
)
from sirtuin.controllers.aws_compute import create_load_balancer_from_prompt
from sirtuin.controllers.aws_container import publish_docker_image_from_config
from sirtuin.controllers.http_headers import print_content_security_policy

cli = typer.Typer()

DEFAULT_CONFIG_FILE: Path = Path("sirtuin.toml")

# ? HTTP Headers


@cli.command()
def generate_csp(
    filepath: Path = typer.Argument(default=DEFAULT_CONFIG_FILE),
) -> None:
    print_content_security_policy(filepath)


# ? Elastic Compute


@cli.command()
def create_load_balancer(
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
def publish_docker_image(
    filepath: Path = typer.Argument(default=DEFAULT_CONFIG_FILE),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    publish_docker_image_from_config(filepath, verbose=verbose)


# ? Elastic Beanstalk


@cli.command()
def create_beanstalk(
    filepath: Path = typer.Argument(default=DEFAULT_CONFIG_FILE),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    create_beanstalk_from_config(filepath, verbose=verbose)


@cli.command()
def upgrade_beanstalk(
    filepath: Path = typer.Argument(default=DEFAULT_CONFIG_FILE),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    upgrade_beanstalk_from_config(filepath, verbose=verbose)


@cli.command()
def deploy_beanstalk(
    filepath: Path = typer.Argument(default=DEFAULT_CONFIG_FILE),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    deploy_beanstalk_from_config(filepath, verbose=verbose)


@cli.command()
def terminate_beanstalk(
    filepath: Path = typer.Argument(default=DEFAULT_CONFIG_FILE),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    terminate_beanstalk_from_config(filepath, verbose=verbose)


# ? Cloudfront


@cli.command()
def deploy_cloudfront(
    filepath: Path = typer.Argument(default=DEFAULT_CONFIG_FILE),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    deploy_cloudfront_from_config(filepath, verbose=verbose)


@cli.command()
def create_invalidation(
    filepath: Path = typer.Argument(default=DEFAULT_CONFIG_FILE),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    invalidate_cloudfront_distribution(filepath, verbose=verbose)
