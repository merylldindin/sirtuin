from pathlib import Path

from sirtuin.models.aws_cloudfront import CloudfrontSirtuinConfig
from sirtuin.utils.decorators import run_command
from sirtuin.utils.loaders import read_toml_file


def _get_sirtuin_config(filepath: Path) -> CloudfrontSirtuinConfig:
    return CloudfrontSirtuinConfig(**read_toml_file(filepath))


@run_command(description="Synchronize application bundle with S3 bucket")
def _synchronize_hosting_bucket(config: CloudfrontSirtuinConfig) -> str:
    return (
        f"aws "
        f"s3 sync {config.application.bundle} "
        f"s3://{config.bucket.name} "
        f"--delete "
        f"--region {config.bucket.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


@run_command(description="Copy application bundle to S3 bucket")
def _copy_application_bundle_to_bucket(config: CloudfrontSirtuinConfig) -> str:
    return (
        f"aws "
        f"s3 cp {config.application.bundle} "
        f"s3://{config.bucket.name} "
        f"--recursive --content-type text/html --exclude *.* "
        f"--region {config.bucket.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


@run_command(description="Invalidate Cloudfront distribution")
def invalidate_cloudfront_distribution(
    filepath: Path, config: CloudfrontSirtuinConfig | None = None
) -> str:
    config = config or _get_sirtuin_config(filepath)

    return (
        f"aws "
        f"cloudfront create-invalidation "
        f"--distribution-id {config.cloudfront.distribution} "
        f"--paths /* "
        f"--region {config.bucket.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


def deploy_cloudfront_from_config(filepath: Path) -> None:
    sirtuin_config = _get_sirtuin_config(filepath)

    _synchronize_hosting_bucket(sirtuin_config)
    _copy_application_bundle_to_bucket(sirtuin_config)
    invalidate_cloudfront_distribution(filepath, config=sirtuin_config)
