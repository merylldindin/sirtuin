from pydantic import BaseModel

from .aws_regions import AwsRegion


class CloudfrontApplicationConfig(BaseModel):
    bundle: str


class CloudfrontBucketConfig(BaseModel):
    name: str
    region: AwsRegion


class CloudfrontDistributionConfig(BaseModel):
    distribution: str


class CloudfrontSirtuinConfig(BaseModel):
    application: CloudfrontApplicationConfig
    bucket: CloudfrontBucketConfig
    cloudfront: CloudfrontDistributionConfig
    directory: str = "."
    profile: str | None = None
