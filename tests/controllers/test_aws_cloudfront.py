from pathlib import Path

from pytest import MonkeyPatch

from sirtuin.controllers import aws_cloudfront


def test_get_sirtuin_config(
    cloudfront_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(cloudfront_sirtuin_config.parent)

    config = aws_cloudfront._get_sirtuin_config(Path(cloudfront_sirtuin_config.name))

    assert config.application.bundle == "my-application-bundle"
    assert config.bucket.name == "my-bucket-name"
    assert config.bucket.region == "us-east-2"
    assert config.cloudfront.distribution == "my-cloudfront-distribution-id"
    assert config.profile == "my-profile"


def test_synchronize_hosting_bucket(
    cloudfront_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(cloudfront_sirtuin_config.parent)

    config = aws_cloudfront._get_sirtuin_config(Path(cloudfront_sirtuin_config.name))

    assert str(aws_cloudfront._synchronize_hosting_bucket(config)).endswith(
        "s3://my-bucket-name --delete --region us-east-2 --profile my-profile"
    )


def test_copy_application_bundle_to_bucket(
    cloudfront_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(cloudfront_sirtuin_config.parent)

    config = aws_cloudfront._get_sirtuin_config(Path(cloudfront_sirtuin_config.name))

    assert str(aws_cloudfront._copy_application_bundle_to_bucket(config)).endswith(
        "s3://my-bucket-name "
        "--recursive --content-type 'text/html' --exclude '*.*' "
        "--region us-east-2 --profile my-profile"
    )


def test_invalidate_cloudfront_distribution(
    cloudfront_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(cloudfront_sirtuin_config.parent)

    assert aws_cloudfront.invalidate_cloudfront_distribution(
        Path(cloudfront_sirtuin_config.name)
    ) == (
        "aws cloudfront create-invalidation "
        "--distribution-id my-cloudfront-distribution-id "
        "--paths '/*' --region us-east-2 --profile my-profile"
    )

    config = aws_cloudfront._get_sirtuin_config(Path(cloudfront_sirtuin_config.name))

    assert aws_cloudfront.invalidate_cloudfront_distribution(
        Path(cloudfront_sirtuin_config.name), config=config
    ) == (
        "aws cloudfront create-invalidation "
        "--distribution-id my-cloudfront-distribution-id "
        "--paths '/*' --region us-east-2 --profile my-profile"
    )
