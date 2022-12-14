import subprocess
import sys
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def if_exists(function: Callable[[Path], T]) -> Callable[[Path], T]:
    def wrapper(filepath: Path, *args: Any, **kwargs: Any) -> T:
        if not filepath.exists():
            raise FileNotFoundError(f"The file {filepath} cannot be found")

        return function(filepath, *args, **kwargs)

    return wrapper


def run_command(
    function: Callable[[T], str]
) -> Callable[[T], CompletedProcess[Any] | str]:
    def wrapper(*args: Any, **kwargs: Any) -> CompletedProcess[Any] | str:
        return (
            function(*args, **kwargs)
            if "pytest" in sys.modules
            else subprocess.run(function(*args, **kwargs).split(" "))
        )

    return wrapper
