from sirtuin.models.aws_compute import LoadBalancerType
from sirtuin.models.aws_regions import AwsRegion
from sirtuin.utils.decorators import run_command


@run_command(description="Create Elastic Load Balancer")
def create_load_balancer_from_prompt(
    name: str, type: str, subnets: str, region: str, profile: str, verbose: bool = False
) -> str:
    return (
        f"aws elbv2 create-load-balancer "
        f"--name {name} "
        f"--type {LoadBalancerType(type).value} "
        f"--subnets {subnets} "
        f"--region {AwsRegion(region).value} "
        + (f"--profile {profile}" if profile is not None else "")
    )
