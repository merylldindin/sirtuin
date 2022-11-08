import os

from pytest import MonkeyPatch

from sirtuin.controllers import aws_cloudfront


def test_get_sirtuin_config(
    cloudfront_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(cloudfront_sirtuin_config))

    config = aws_cloudfront._get_sirtuin_config(
        os.path.basename(cloudfront_sirtuin_config)
    )

    assert config.application.bundle == "my-application-bundle"
    assert config.bucket.name == "my-bucket-name"
    assert config.bucket.region == "us-east-2"
    assert config.cloudfront.distribution == "my-cloudfront-distribution-id"
    assert config.profile == "my-profile"


def test_synchronize_hosting_bucket(
    cloudfront_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(cloudfront_sirtuin_config))

    config = aws_cloudfront._get_sirtuin_config(
        os.path.basename(cloudfront_sirtuin_config)
    )

    assert str(aws_cloudfront._synchronize_hosting_bucket(config)).endswith(
        "s3://my-bucket-name --delete --region us-east-2 --profile my-profile"
    )


def test_copy_application_bundle_to_bucket(
    cloudfront_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(cloudfront_sirtuin_config))

    config = aws_cloudfront._get_sirtuin_config(
        os.path.basename(cloudfront_sirtuin_config)
    )

    assert str(aws_cloudfront._copy_application_bundle_to_bucket(config)).endswith(
        "s3://my-bucket-name "
        "--recursive --content-type 'text/html' --exclude '*.*' "
        "--region us-east-2 --profile my-profile"
    )


def test_invalidate_cloudfront_distribution(
    cloudfront_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(cloudfront_sirtuin_config))

    assert aws_cloudfront.invalidate_cloudfront_distribution(
        os.path.basename(cloudfront_sirtuin_config)
    ) == (
        "aws cloudfront create-invalidation "
        "--distribution-id my-cloudfront-distribution-id "
        "--paths '/*' --region us-east-2 --profile my-profile"
    )

    config = aws_cloudfront._get_sirtuin_config(
        os.path.basename(cloudfront_sirtuin_config)
    )

    assert aws_cloudfront.invalidate_cloudfront_distribution(
        os.path.basename(cloudfront_sirtuin_config), config=config
    ) == (
        "aws cloudfront create-invalidation "
        "--distribution-id my-cloudfront-distribution-id "
        "--paths '/*' --region us-east-2 --profile my-profile"
    )
