import sys
from pathlib import Path
from subprocess import Popen
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def if_exists(function: Callable[[Path], T]) -> Callable[[Path], T]:
    def wrapper(filepath: Path, *args: Any, **kwargs: Any) -> T:
        if not filepath.exists():
            raise FileNotFoundError(f"The file {filepath} cannot be found")

        return function(filepath, *args, **kwargs)

    return wrapper


def run_command(function: Callable[[T], str]) -> Callable[[T], int | str]:
    def wrapper(*args: Any, **kwargs: Any) -> int | str:
        return (
            function(*args, **kwargs)
            if "pytest" in sys.modules
            else Popen(function(*args, **kwargs)).wait()
        )

    return wrapper
