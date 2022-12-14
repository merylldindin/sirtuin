import json
import shutil
from enum import Enum
from pathlib import Path, PosixPath
from typing import Any

import yaml
from yaml import SafeDumper


def _ensure_directory_existence(filepath: Path) -> None:
    filepath.parent.mkdir(exist_ok=True, parents=True)


def dump_as_json(content: dict[Any, Any], filepath: Path) -> None:
    _ensure_directory_existence(filepath)

    with open(filepath, mode="w", encoding="utf-8") as stream:
        json.dump(content, stream, indent=2)


class CustomYamlDumper(SafeDumper):
    def represent_data(self, data: Any) -> Any:
        if isinstance(data, Enum):
            return self.represent_data(data.value)

        if isinstance(data, PosixPath):
            return self.represent_data(str(data))

        return super().represent_data(data)


def dump_as_yaml(content: dict[Any, Any], filepath: Path) -> None:
    _ensure_directory_existence(filepath)

    with open(filepath, mode="w", encoding="utf-8") as stream:
        yaml.dump(content, stream, Dumper=CustomYamlDumper)


def dump_as_raw(content: str, filepath: Path) -> None:
    _ensure_directory_existence(filepath)

    with open(filepath, mode="w", encoding="utf-8") as stream:
        stream.write(content)


def copy_file(source: Path, destination: Path) -> None:
    _ensure_directory_existence(destination)

    shutil.copyfile(source, destination)
