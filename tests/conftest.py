from pathlib import Path

import pytest

DEFAULT_PATH_TO_FIXTURES = Path("tests/fixtures")


@pytest.fixture
def cloudfront_sirtuin_config() -> Path:
    return DEFAULT_PATH_TO_FIXTURES / "cloudfront/sirtuin.toml"


@pytest.fixture
def container_sirtuin_config() -> Path:
    return DEFAULT_PATH_TO_FIXTURES / "container/sirtuin.toml"


@pytest.fixture
def headers_sirtuin_config() -> Path:
    return DEFAULT_PATH_TO_FIXTURES / "headers/sirtuin.toml"
