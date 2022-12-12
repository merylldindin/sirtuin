import os
import sys
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def if_exists(function: Callable[[str], T]) -> Callable[[str], T]:
    def wrapper(filepath: str, *args: Any, **kwargs: Any) -> T:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file {filepath} cannot be found")

        return function(filepath, *args, **kwargs)

    return wrapper

def run_command(function: Callable[[T], str]) -> Callable[[T], int | str]:
    def wrapper(*args: Any, **kwargs: Any) -> int | str:
        return (
            function(*args, **kwargs)
            if "pytest" in sys.modules
            else os.system(function(*args, **kwargs))
        )

    return wrapper

