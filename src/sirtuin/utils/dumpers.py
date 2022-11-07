import json
import os
import shutil
from enum import Enum
from typing import Any

import yaml
from yaml import SafeDumper


def _ensure_directory_existence(filepath: str) -> None:
    directory_name = os.path.dirname(filepath)

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def dump_as_json(content: dict, filepath: str) -> None:
    _ensure_directory_existence(filepath)

    with open(filepath, mode="w", encoding="utf-8") as stream:
        json.dump(content, stream, indent=2)


class CustomYamlDumper(SafeDumper):
    def represent_data(self, data: Any) -> Any:
        if isinstance(data, Enum):
            return self.represent_data(data.value)

        return super().represent_data(data)


def dump_as_yaml(content: dict, filepath: str) -> None:
    _ensure_directory_existence(filepath)

    with open(filepath, mode="w", encoding="utf-8") as stream:
        yaml.dump(content, stream, Dumper=CustomYamlDumper)


def dump_as_raw(content: str, filepath: str) -> None:
    _ensure_directory_existence(filepath)

    with open(filepath, mode="w", encoding="utf-8") as stream:
        stream.write(content)


def copy_file(source: str, destination: str) -> None:
    _ensure_directory_existence(destination)

    shutil.copyfile(source, destination)
