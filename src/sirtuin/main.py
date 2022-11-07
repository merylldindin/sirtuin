import typer

from sirtuin.controllers.http_headers import print_content_security_policy

cli = typer.Typer()


# ? HTTP Headers


@cli.command()
def generate_csp(
    filepath: str = typer.Argument(default="sirtuin.toml"),
) -> None:
    print_content_security_policy(filepath)


# ? Elastic Beanstalk


@cli.command()
def create_beanstalk(
    filepath: str = typer.Argument(default="sirtuin.toml"),
) -> None:
    pass


@cli.command()
def upgrade_beanstalk(
    filepath: str = typer.Argument(default="sirtuin.toml"),
) -> None:
    pass


@cli.command()
def deploy_beanstalk(
    filepath: str = typer.Argument(default="sirtuin.toml"),
) -> None:
    pass


@cli.command()
def terminate_beanstalk(
    filepath: str = typer.Argument(default="sirtuin.toml"),
) -> None:
    pass


# ? Cloudfront


@cli.command()
def deploy_cloudfront(
    filepath: str = typer.Argument(default="sirtuin.toml"),
) -> None:
    pass
