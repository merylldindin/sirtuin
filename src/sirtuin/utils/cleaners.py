import os
import shutil

from .decorators import if_exists


@if_exists
def delete_file(filepath: str) -> None:
    os.remove(filepath)


def delete_directory(directory: str) -> None:
    if os.path.isdir(directory):
        shutil.rmtree(directory)
