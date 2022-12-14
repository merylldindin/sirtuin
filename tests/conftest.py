import os

import pytest

DEFAULT_PATH_TO_FIXTURES = "tests/fixtures"

@pytest.fixture
def cli_directory() -> str:
    return os.path.join(os.getcwd(), "src/sirtuin/schemas")


@pytest.fixture
def beanstalk_sirtuin_config() -> str:
    return f"{DEFAULT_PATH_TO_FIXTURES}/beanstalk/sirtuin.toml"


@pytest.fixture
def cloudfront_sirtuin_config() -> str:
    return f"{DEFAULT_PATH_TO_FIXTURES}/cloudfront/sirtuin.toml"


@pytest.fixture
def gateway_sirtuin_config() -> str:
    return f"{DEFAULT_PATH_TO_FIXTURES}/gateway/sirtuin.toml"


@pytest.fixture
def headers_sirtuin_config() -> str:
    return f"{DEFAULT_PATH_TO_FIXTURES}/headers/sirtuin.toml"
