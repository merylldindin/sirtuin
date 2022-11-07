import os

from utils.constants import IRRELEVANT_FILES
from utils.exceptions import ConfigException


def get_filepaths(root_directories: list[str]) -> dict[str, str]:
    filepaths = {}
    for root_directory in root_directories:
        for root_path, _, files in os.walk(root_directory):
            for filename in files:
                if filename in IRRELEVANT_FILES:
                    continue

                if filename in filepaths:
                    raise ConfigException(f"Duplicate filename {filename}")

                filepaths[filename] = os.path.join(root_path, filename)

    return filepaths


def find_filepath(filename: str, filepaths: dict[str, str]) -> str:
    if filename not in filepaths:
        raise ConfigException(f"Configuration file {filename} not found")

    return filepaths[filename]
