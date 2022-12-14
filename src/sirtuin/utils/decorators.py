import subprocess
import sys
from pathlib import Path
from subprocess import CompletedProcess
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
) -> Callable[..., Callable[[T], str | CompletedProcess[Any]]]:
    def decorator(
        function: Callable[[T], str]
    ) -> Callable[[T], str | CompletedProcess[Any]]:
        def wrapper(*args: Any, **kwargs: Any) -> str | CompletedProcess[Any]:
            if "pytest" in sys.modules:
                return function(*args, **kwargs)

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                transient=True,
            ) as spinner:
                spinner.add_task(description=description, total=None)

                return subprocess.run(function(*args, **kwargs).split(" "))

        return wrapper

    return decorator
