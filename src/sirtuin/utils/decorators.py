import os
import sys
from typing import Any, Callable


def if_exists(function: Callable[[str], Any]) -> Callable[[Any], Any]:
    def wrapper(filepath: str, *args, **kwargs) -> Any:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file {filepath} cannot be found")

        return function(filepath, *args, **kwargs)

    return wrapper


def run_command(function: Callable[[Any], str]) -> Callable[[Any], int | str]:
    def wrapper(*args, **kwargs) -> int | str:
        return (
            function(*args, **kwargs)
            if "pytest" in sys.modules
            else os.system(function(*args, **kwargs))
        )

    return wrapper
