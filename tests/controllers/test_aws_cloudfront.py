from sirtuin.controllers import aws_cloudfront


def test_get_sirtuin_config(cloudfront_sirtuin_config: str) -> None:
    config = aws_cloudfront._get_sirtuin_config(cloudfront_sirtuin_config)

    assert config.application.bundle == "my-application-bundle"
    assert config.bucket.name == "my-bucket-name"
    assert config.bucket.region == "us-east-2"
    assert config.directory == "tests/fixtures/cloudfront"
    assert config.cloudfront.distribution == "my-cloudfront-distribution-id"
    assert config.profile == "my-profile"


def test_synchronize_hosting_bucket(cloudfront_sirtuin_config: str) -> None:
    config = aws_cloudfront._get_sirtuin_config(cloudfront_sirtuin_config)

    assert aws_cloudfront._synchronize_hosting_bucket(config) == (
        "aws s3 sync tests/fixtures/cloudfront/my-application-bundle "
        "s3://my-bucket-name "
        "--delete --region us-east-2 --profile my-profile"
    )


def test_copy_application_bundle_to_bucket(cloudfront_sirtuin_config: str) -> None:
    config = aws_cloudfront._get_sirtuin_config(cloudfront_sirtuin_config)

    assert aws_cloudfront._copy_application_bundle_to_bucket(config) == (
        "aws s3 cp tests/fixtures/cloudfront/my-application-bundle "
        "s3://my-bucket-name "
        "--recursive --content-type 'text/html' --exclude '*.*' "
        "--region us-east-2 --profile my-profile"
    )


def test_invalidate_cloudfront_distribution(cloudfront_sirtuin_config: str) -> None:
    config = aws_cloudfront._get_sirtuin_config(cloudfront_sirtuin_config)

    assert aws_cloudfront._invalidate_cloudfront_distribution(config) == (
        "aws cloudfront create-invalidation "  # noqa: F541
        "--distribution-id my-cloudfront-distribution-id "
        "--paths '/*' --region us-east-2 --profile my-profile"
    )
