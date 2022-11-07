import typer

from sirtuin.controllers.http_headers import print_content_security_policy

cli = typer.Typer()


@cli.command()
def generate_content_security_policy(
    filepath: str = typer.Argument(default="sirtuin.toml"),
) -> None:
    print_content_security_policy(filepath)


@cli.command()
def test(filepath: str = typer.Argument(default="sirtuin.toml")) -> None:
    print_content_security_policy(filepath)
