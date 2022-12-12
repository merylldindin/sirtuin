from sirtuin.controllers import aws_compute


def test_create_application_load_balancer() -> None:
    assert aws_compute.create_load_balancer_from_prompt(
        "LOAD-BALANCER",
        "application",
        "subnet-123 subnet-456",
        "us-east-1",
        "my-profile"
    ) == (
        "aws elbv2 create-load-balancer "
        "--name LOAD-BALANCER "
        "--type application "
        "--subnets subnet-123 subnet-456 "
        "--region us-east-1 "
        "--profile my-profile"
    )

def test_create_network_load_balancer() -> None:
    assert aws_compute.create_load_balancer_from_prompt(
        "LOAD-BALANCER",
        "network",
        "subnet-123 subnet-456",
        "us-east-1",
        "my-profile"
    ) == (
        "aws elbv2 create-load-balancer "
        "--name LOAD-BALANCER "
        "--type network "
        "--subnets subnet-123 subnet-456 "
        "--region us-east-1 "
        "--profile my-profile"
    )
