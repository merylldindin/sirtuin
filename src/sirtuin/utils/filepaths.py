import os
import subprocess


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
