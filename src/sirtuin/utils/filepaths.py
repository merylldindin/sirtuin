import os
import subprocess
from pathlib import Path


def get_service_directory(filepath: str, config_directory: str = ".") -> str:
    service_directory = os.path.dirname(filepath)
    for _ in range(len(Path(config_directory).parents)):
        service_directory = os.path.dirname(service_directory)

    return service_directory


def _get_virtual_environment_path() -> str:
    try:
        return subprocess.check_output(["poetry env info", "--path"]).decode()[:-1]
    except Exception:
        return os.path.join(os.getcwd(), ".venv")


def get_schemas_path() -> str:
    filepath = os.path.join(
        _get_virtual_environment_path(),
        "lib",
        "python3.10",
        "site-packages",
        "sirtuin",
        "schemas",
    )

    if not os.path.exists(filepath):
        return os.path.join(os.getcwd(), "src", "sirtuin", "schemas")

    return filepath
