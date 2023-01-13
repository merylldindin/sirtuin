from pathlib import Path

from pydantic import BaseModel, Field, PositiveInt

from .aws_instances import AwsInstance
from .aws_regions import AwsRegion
from .base_models import SanitizedBaseModel

DEFAULT_BEANSTALK_ARTIFACT_PATH: Path = Path("artifact.zip")
DEFAULT_BEANSTALK_CONFIG_DIRECTORY: Path = Path(".elasticbeanstalk")
DEFAULT_BEANSTALK_CONFIG_PATH: Path = DEFAULT_BEANSTALK_CONFIG_DIRECTORY / "config.yml"
DEFAULT_BEANSTALK_DOCKERRUN_PATH: Path = Path("Dockerrun.aws.json")
DEFAULT_BEANSTALK_EBEXTENSIONS_DIRECTORY: Path = Path(".ebextensions")
DEFAULT_BEANSTALK_EBEXTENSIONS_SCHEMAS: Path = Path("ebextensions")
DEFAULT_BEANSTALK_EBIGNORE_PATH: Path = Path(".ebignore")
DEFAULT_BEANSTALK_PLATFORM: str = "Docker running on 64bit Amazon Linux 2"
DEFAULT_BEANSTALK_PLATFORM_DIRECTORY: Path = Path(".platform")
DEFAULT_BEANSTALK_PLATFORM_SCHEMAS: Path = Path("platform")

# ? .elasticbeanstalk/config.yml


class ElasticBeanstalkGlobalConfig(BaseModel):
    application: str = Field(alias="application_name")
    ec2_keyname: str = Field(alias="default_ec2_keyname")
    platform: str = Field(default=DEFAULT_BEANSTALK_PLATFORM, alias="default_platform")
    profile: str
    region: str = Field(alias="default_region")
    workspace: str = Field(default="Application", alias="workspace_type")


class ElasticBeanstalkEnvironment(BaseModel):
    environment: str


class ElasticBeanstalkBranchConfig(BaseModel):
    default: ElasticBeanstalkEnvironment


class ElasticBeanstalkArtifact(BaseModel):
    artifact: Path = Field(default=DEFAULT_BEANSTALK_ARTIFACT_PATH)


class ElasticBeanstalkConfig(BaseModel):
    branch: ElasticBeanstalkBranchConfig = Field(alias="branch-defaults")
    deploy: ElasticBeanstalkArtifact = Field(default=ElasticBeanstalkArtifact())
    config: ElasticBeanstalkGlobalConfig = Field(alias="global")


# ? Dockerrun.aws.json


class ElasticBeanstalkDockerrunPort(SanitizedBaseModel):
    container: int = Field(alias="ContainerPort")
    host: int = Field(alias="HostPort")


class ElasticBeanstalkDockerrunVolume(SanitizedBaseModel):
    container: str = Field(alias="ContainerDirectory")
    host: str = Field(alias="HostDirectory")


class ElasticBeanstalkDockerrunImage(SanitizedBaseModel):
    name: str = Field(alias="Name")
    update: bool = Field(default=True, alias="Update")


class ElasticBeanstalkDockerrunAuthentication(SanitizedBaseModel):
    bucket: str = Field(alias="Bucket")
    key: str = Field(alias="Key")


class ElasticBeanstalkDockerrunConfig(SanitizedBaseModel):
    authentication: ElasticBeanstalkDockerrunAuthentication | None = Field(
        None, alias="Authentication"
    )
    aws_eb_dockerrun_version: int = Field(default=1, alias="AWSEBDockerrunVersion")
    image: ElasticBeanstalkDockerrunImage = Field(alias="Image")
    ports: list[ElasticBeanstalkDockerrunPort] = Field(alias="Ports")
    volumes: list[ElasticBeanstalkDockerrunVolume] = Field(default=[], alias="Volumes")


# ? sirtuin.toml


class ElasticBeanstalkServiceConfig(BaseModel):
    application: str = Field(alias="ApplicationName")
    ec2_keyname: str = Field(alias="EC2KeyName")
    service: str = Field(alias="ServiceName")
    dotenv_path: Path | None = Field(default=None, alias="DotenvPath")


class ElasticBeanstalkDockerPort(BaseModel):
    container: PositiveInt
    host: PositiveInt


class ElasticBeanstalkDockerVolume(BaseModel):
    container: str
    host: str


class ElasticBeanstalkDockerConfig(BaseModel):
    image: str = Field(alias="Image")
    auth_bucket: str | None = Field(None, alias="AuthBucket")
    auth_key: str | None = Field(None, alias="AuthKey")
    ports: list[ElasticBeanstalkDockerPort] = Field(alias="Ports")
    volumes: list[ElasticBeanstalkDockerVolume] = Field(alias="Volumes")


class ElasticBeanstalkInstanceConfig(BaseModel):
    instance_type: AwsInstance = Field(alias="InstanceType")
    min_instances: PositiveInt = Field(default=1, alias="MinInstances")
    max_instances: PositiveInt = Field(default=1, alias="MaxInstances")
    region: AwsRegion = Field(alias="Region")
    timeout: PositiveInt = Field(default=30, alias="Timeout")


class ElasticBeanstalkLoadBalancerConfig(BaseModel):
    is_shared: bool = Field(default=False, alias="IsShared")
    elb_type: str = Field(default="application", alias="ElbType")
    shared_elb_name: str | None = Field(default=None, alias="SharedElbName")
    shared_elb_port: PositiveInt | None = Field(default=None, alias="SharedElbPort")


class ElasticBeanstalkVpcConfig(BaseModel):
    db_subnets: str = Field(alias="DbSubnets")
    ec2_subnets: str = Field(alias="Ec2Subnets")
    elb_subnets: str = Field(alias="ElbSubnets")
    vpc_id: str = Field(alias="VpcId")


class ElasticBeanstalkSirtuinConfig(BaseModel):
    beanstalk: ElasticBeanstalkServiceConfig
    docker: ElasticBeanstalkDockerConfig
    ebextensions: dict[str, dict[str, str | int] | None]
    instance: ElasticBeanstalkInstanceConfig
    load_balancer: ElasticBeanstalkLoadBalancerConfig = Field(alias="load-balancer")
    platform: dict[str, dict[str, str | int] | None]
    profile: str = Field(alias="Profile")
    vpc: ElasticBeanstalkVpcConfig
