from pathlib import Path

from sirtuin.models.aws_cloudfront import CloudfrontSirtuinConfig
from sirtuin.utils.constants import DEFAULT_AWS_PROFILE
from sirtuin.utils.decorators import catch_remote_config, run_command
from sirtuin.utils.loaders import read_toml_file


def _get_sirtuin_config(filepath: Path) -> CloudfrontSirtuinConfig:
    return CloudfrontSirtuinConfig(**read_toml_file(filepath))


@run_command(description="Synchronize application bundle with S3 bucket")
def _synchronize_hosting_bucket(
    config: CloudfrontSirtuinConfig, verbose: bool = False
) -> str:
    return (
        f"aws "
        f"s3 sync {config.application.bundle} "
        f"s3://{config.bucket.name} "
        f"--delete "
        f"--region {config.bucket.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


@run_command(description="Copy application bundle to S3 bucket")
def _copy_application_bundle_to_bucket(
    config: CloudfrontSirtuinConfig, verbose: bool = False
) -> str:
    return (
        f"aws "
        f"s3 cp {config.application.bundle} "
        f"s3://{config.bucket.name} "
        f"--recursive --content-type text/html --exclude *.* "
        f"--region {config.bucket.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


@run_command(description="Invalidate Cloudfront distribution")
def _invalidate_cloudfront_distribution(
    config: CloudfrontSirtuinConfig, verbose: bool = False
) -> str:
    return (
        f"aws "
        f"cloudfront create-invalidation "
        f"--distribution-id {config.cloudfront.distribution} "
        f"--paths /* "
        f"--region {config.bucket.region.value} "
        + (f"--profile {config.profile}" if config.profile is not None else "")
    )


@catch_remote_config
def invalidate_cloudfront_from_config(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    sirtuin_config = _get_sirtuin_config(filepath)

    _invalidate_cloudfront_distribution(sirtuin_config, verbose=verbose)


@catch_remote_config
def deploy_cloudfront_from_config(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    sirtuin_config = _get_sirtuin_config(filepath)

    _synchronize_hosting_bucket(sirtuin_config, verbose=verbose)
    _copy_application_bundle_to_bucket(sirtuin_config, verbose=verbose)
    _invalidate_cloudfront_distribution(sirtuin_config, verbose=verbose)
