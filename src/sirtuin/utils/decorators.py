import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, TypeVar

from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

T = TypeVar("T")


def if_exists(function: Callable[[Path], T]) -> Callable[[Path], T]:
    def wrapper(filepath: Path, *args: Any, **kwargs: Any) -> T:
        if not filepath.exists():
            raise FileNotFoundError(f"The file {filepath} cannot be found")

        return function(filepath, *args, **kwargs)

    return wrapper


def run_command(
    description: str,
) -> Callable[..., Callable[[T], str | tuple[bytes, bytes]]]:
    def decorator(
        function: Callable[[T], str]
    ) -> Callable[[T], str | tuple[bytes, bytes]]:
        def wrapper(*args: Any, **kwargs: Any) -> str | tuple[bytes, bytes]:
            if "pytest" in sys.modules:
                return function(*args, **kwargs)

            if kwargs["verbose"]:
                return subprocess.Popen(
                    function(*args, **kwargs), shell=True
                ).communicate()

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
            ) as spinner:
                spinner.add_task(description=description, total=None)

                return subprocess.Popen(
                    function(*args, **kwargs),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    shell=True,
                ).communicate()

        return wrapper

    return decorator
