import os
import shutil


def delete_file(filepath: str) -> None:
    if os.path.isfile(filepath):
        os.remove(filepath)


def delete_directory(directory: str) -> None:
    if os.path.isdir(directory):
        shutil.rmtree(directory)
