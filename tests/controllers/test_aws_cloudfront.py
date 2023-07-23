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


def test_synchronize_bundle_engine(
    cloudfront_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(cloudfront_sirtuin_config.parent)

    config = aws_cloudfront._get_sirtuin_config(Path(cloudfront_sirtuin_config.name))

    assert str(aws_cloudfront._synchronize_bundle_engine(config, False)).endswith(
        "s3://my-bucket-name/_nuxt/ "
        "--cache-control 'max-age=31536000,public,immutable' "
        "--delete "
        "--region us-east-2 "
        "--profile my-profile"
    )


def test_synchronize_bundle_assets(
    cloudfront_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(cloudfront_sirtuin_config.parent)

    config = aws_cloudfront._get_sirtuin_config(Path(cloudfront_sirtuin_config.name))

    assert str(aws_cloudfront._synchronize_bundle_assets(config, False)).endswith(
        "s3://my-bucket-name "
        "--exclude '_nuxt/*' "
        "--cache-control 'max-age=0,public,must-revalidate' "
        "--delete "
        "--region us-east-2 "
        "--profile my-profile"
    )


def test_invalidate_cloudfront_distribution(
    cloudfront_sirtuin_config: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(cloudfront_sirtuin_config.parent)

    config = aws_cloudfront._get_sirtuin_config(Path(cloudfront_sirtuin_config.name))

    assert aws_cloudfront._invalidate_cloudfront_distribution(config, False) == (
        "aws cloudfront create-invalidation "
        "--distribution-id my-cloudfront-distribution-id "
        "--paths '/*' --region us-east-2 --profile my-profile"
    )
