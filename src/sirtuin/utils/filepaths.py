import sysconfig
from pathlib import Path


def _get_sitepackage_path() -> Path:
    sitepackages_directory = Path(sysconfig.get_paths()["purelib"])

    if (sitepackages_directory / "sirtuin").exists():
        return sitepackages_directory / "sirtuin"

    return Path(sysconfig.get_paths()["data"]).parent / "src/sirtuin"


def get_schemas_path() -> Path:
    return _get_sitepackage_path() / "schemas"
