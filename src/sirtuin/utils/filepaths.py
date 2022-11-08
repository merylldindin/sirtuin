import os
import subprocess


def get_service_directory() -> str:
    return os.getcwd()


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
        package_root = os.getcwd()
        while not package_root.endswith("sirtuin"):
            package_root = os.path.dirname(package_root)

        return os.path.join(package_root, "src", "sirtuin", "schemas")

    return filepath
