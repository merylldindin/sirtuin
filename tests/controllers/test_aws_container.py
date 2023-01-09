from pathlib import Path

from pytest import MonkeyPatch

from sirtuin.controllers import aws_container


def test_get_sirtuin_config(
    container_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(container_sirtuin_config.parent)

    config = aws_container._get_sirtuin_config(Path(container_sirtuin_config.name))

    assert config.profile == "my-profile"
    assert config.cluster.name == "my-cluster"
    assert config.cluster.region.value == "us-east-2"
    assert config.image.source == "source:tag"
    assert config.image.target == "target:tag"
    assert config.registry.account == "123456789012.dkr.ecr.us-east-2.amazonaws.com"
    assert config.registry.region.value == "us-east-2"


def test_login_container_registry(
    container_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(container_sirtuin_config.parent)

    config = aws_container._get_sirtuin_config(Path(container_sirtuin_config.name))

    assert aws_container._login_container_registry(config) == (
        "aws ecr get-login-password "
        "--region us-east-2 "
        "--profile my-profile "
        "| docker login "
        "--username AWS "
        "--password-stdin 123456789012.dkr.ecr.us-east-2.amazonaws.com"
    )


def test_tag_docker_image(
    container_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(container_sirtuin_config.parent)

    config = aws_container._get_sirtuin_config(Path(container_sirtuin_config.name))

    assert aws_container._tag_docker_image(config) == (
        "docker tag source:tag 123456789012.dkr.ecr.us-east-2.amazonaws.com/target:tag"
    )


def test_push_docker_image(
    container_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(container_sirtuin_config.parent)

    config = aws_container._get_sirtuin_config(Path(container_sirtuin_config.name))

    assert aws_container._push_docker_image(config) == (
        "docker push 123456789012.dkr.ecr.us-east-2.amazonaws.com/target:tag"
    )


def test_untag_docker_image(
    container_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(container_sirtuin_config.parent)

    config = aws_container._get_sirtuin_config(Path(container_sirtuin_config.name))

    assert aws_container._untag_docker_image(config) == (
        "docker rmi 123456789012.dkr.ecr.us-east-2.amazonaws.com/target:tag"
    )
