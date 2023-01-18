import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, TypeVar

from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from pydantic import BaseModel

from .constants import DEFAULT_SIRTUIN_CONFIG_NAME

T = TypeVar("T")
S = TypeVar("S", bound=BaseModel)


def if_exists(function: Callable[[Path], T]) -> Callable[[Path], T]:
    def wrapper(filepath: Path, *args: Any, **kwargs: Any) -> T:
        if not filepath.exists():
            raise FileNotFoundError(f"The file {filepath} cannot be found")

        return function(filepath, *args, **kwargs)

    return wrapper


def run_interactive_subprocess(description: str, command: str) -> None:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    ) as spinner:
        spinner.add_task(description=description, total=None)

        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            shell=True,
        ).communicate()


def run_command(
    description: str,
) -> Callable[..., Callable[[S, bool], str]]:
    def decorator(function: Callable[[S, bool], str]) -> Callable[[S, bool], str]:
        def wrapper(*args: Any, **kwargs: Any) -> str:
            if "pytest" in sys.modules:
                return function(*args, **kwargs)

            subprocess.Popen(
                function(*args, **kwargs), shell=True
            ).communicate() if args[1] else run_interactive_subprocess(
                description, function(*args, **kwargs)
            )

            return "OK"

        return wrapper

    return decorator


def _load_config_from_s3(file_arn: str, profile: str) -> None:
    return run_interactive_subprocess(
        "Loading configuration from S3",
        f"aws s3 cp {file_arn} {DEFAULT_SIRTUIN_CONFIG_NAME} --profile {profile}",
    )


def catch_remote_config(
    function: Callable[[Path, str, bool], T]
) -> Callable[[str, str, bool], T]:
    def wrapper(*args: Any) -> Any:
        filepath, profile, verbose = args

        if filepath.startswith("s3://"):
            _load_config_from_s3(filepath, profile)

            result = function(Path(DEFAULT_SIRTUIN_CONFIG_NAME), profile, verbose)

            Path(DEFAULT_SIRTUIN_CONFIG_NAME).unlink()

            return result

        return function(Path(filepath), profile, verbose)

    return wrapper
