from pydantic import BaseModel, Field

from .aws_regions import AwsRegion


class CloudfrontApplicationConfig(BaseModel):
    bundle: str = Field(alias="Bundle")


class CloudfrontBucketConfig(BaseModel):
    name: str = Field(alias="Name")
    region: AwsRegion = Field(alias="Region")


class CloudfrontDistributionConfig(BaseModel):
    distribution: str = Field(alias="Distribution")


class CloudfrontSirtuinConfig(BaseModel):
    application: CloudfrontApplicationConfig
    bucket: CloudfrontBucketConfig
    cloudfront: CloudfrontDistributionConfig
    profile: str | None = Field(default=None, alias="Profile")
