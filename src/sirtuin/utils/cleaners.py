import shutil
from pathlib import Path


def delete_file(filepath: Path) -> None:
    if filepath.is_file():
        filepath.unlink()


def delete_directory(directory: Path) -> None:
    if directory.is_dir():
        shutil.rmtree(directory)
