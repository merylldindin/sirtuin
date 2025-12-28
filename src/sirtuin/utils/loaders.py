import json
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import tomli
import yaml

from .decorators import if_exists


@if_exists
def read_json_file(filepath: Path) -> dict[str, Any]:
    with open(filepath, mode="r", encoding="utf-8") as raw_file:
        return json.load(raw_file)


@if_exists
def read_dotenv_file(filepath: Path) -> dict[str, str]:
    with open(filepath, mode="r", encoding="utf-8") as raw_file:
        variables = map(
            lambda line: [item.strip() for item in line.split("=")],
            [line for line in raw_file.readlines() if line != "\n"],
        )

    return {variable[0]: variable[1] for variable in variables}


@if_exists
def read_raw_file(filepath: Path) -> str:
    with open(filepath, mode="r", encoding="utf-8") as raw_file:
        return raw_file.read()


@if_exists
def read_toml_file(filepath: Path) -> dict[str, Any]:
    with open(filepath, mode="rb") as raw_file:
        return tomli.load(raw_file)


@if_exists
def read_yaml_file(filepath: Path) -> dict[str, Any]:
    with open(filepath, mode="r", encoding="utf-8") as raw_file:
        return yaml.safe_load(raw_file)


@if_exists
def list_zip_files(filepath: Path) -> list[str]:
    with ZipFile(filepath, mode="r") as zip_file:
        return zip_file.namelist()
