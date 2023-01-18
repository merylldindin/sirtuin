from pydantic import BaseModel, Field

from .aws_regions import AwsRegion


class ElasticContainerRegistryConfig(BaseModel):
    account: str = Field(alias="Account")
    region: AwsRegion = Field(alias="Region")


class ElasticContainerImageConfig(BaseModel):
    source: str = Field(alias="Source")
    target: str = Field(alias="Target")


class ElasticContainerClusterConfig(BaseModel):
    name: str = Field(alias="Name")
    region: AwsRegion = Field(alias="Region")
    service: str = Field(alias="Service")


class ElasticContainerServiceConfig(BaseModel):
    registry: ElasticContainerRegistryConfig
    image: ElasticContainerImageConfig
    cluster: ElasticContainerClusterConfig
    profile: str = Field(alias="Profile")
