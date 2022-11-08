import os

from pytest import MonkeyPatch

from sirtuin.controllers import aws_beanstalk
from sirtuin.models.aws_instances import AwsInstance
from sirtuin.utils.loaders import (
    list_zip_files,
    read_json_file,
    read_raw_file,
    read_yaml_file,
)


def test_get_sirtuin_config(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    assert config.beanstalk.application == "my-application"
    assert config.docker.image == "my-dockerhub-repository/my-image"
    assert "autoscaling.config" in config.ebextensions
    assert config.instance.instance_type == AwsInstance.T3_SMALL
    assert config.load_balancer.shared_alb_port == 443
    assert "hooks/prebuild/set_timezone.sh" in config.platform
    assert config.profile == "my-profile"
    assert config.vpc.vpc_id == "my-vpc-id"


def test_get_environment_variables(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    assert config.beanstalk.dotenv_path == ".env"

    variables = aws_beanstalk._get_environment_variables(config)

    assert variables is not None
    assert variables["KEY"] == "VARIABLE"


def test_write_ebignore_config(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    filepath = aws_beanstalk._write_ebignore_config(config)

    assert os.path.exists(filepath)
    assert read_raw_file(filepath) == "*\n\n!artifact.zip"

    aws_beanstalk._clean_beanstalk_deployment(config)


def test_write_beanstalk_config(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    filepath = aws_beanstalk._write_beanstalk_config(config)

    assert os.path.exists(filepath)
    beanstalk = read_yaml_file(filepath)
    assert beanstalk["deploy"]["artifact"] == "artifact.zip"
    assert beanstalk["branch-defaults"]["default"]["environment"] == "my-service"
    assert beanstalk["global"]["application_name"] == "my-application"
    assert beanstalk["global"]["workspace_type"] == "Application"

    aws_beanstalk._clean_beanstalk_deployment(config)


def test_write_dockerrun_config(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    filepath = aws_beanstalk._write_dockerrun_config(config)

    assert os.path.exists(filepath)
    dockerrun = read_json_file(filepath)
    assert dockerrun["AWSEBDockerrunVersion"] == "1"
    assert dockerrun["Image"]["Name"] == "my-dockerhub-repository/my-image"
    assert dockerrun["Image"]["Update"] == "true"
    assert dockerrun["Ports"][0]["ContainerPort"] == "5000"
    assert dockerrun["Authentication"]["Bucket"] == "my-bucket"

    aws_beanstalk._clean_beanstalk_deployment(config)


def test_write_beanstalk_customization(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    filepaths = aws_beanstalk._write_beanstalk_customization(config)

    assert len(filepaths) == 9

    assert any(
        filepath.endswith(".ebextensions/autoscaling.config") for filepath in filepaths
    )
    assert any(
        filepath.endswith(".ebextensions/security.config") for filepath in filepaths
    )
    assert any(
        filepath.endswith(".platform/nginx/conf.d/sizes.conf") for filepath in filepaths
    )

    security = read_yaml_file(".ebextensions/security.config")

    assert (
        security["option_settings"]["aws:autoscaling:launchconfiguration"]["EC2KeyName"]
        == "my-ec2-keyname"
    )

    aws_beanstalk._clean_beanstalk_deployment(config)


def test_setup_beanstalk_deployment(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    filepath = aws_beanstalk._setup_beanstalk_deployment(config)

    assert os.path.exists(filepath)

    zip_files = list_zip_files(filepath)
    assert any(filepath.startswith(".ebextensions/") for filepath in zip_files)
    assert any(filepath.startswith(".platform/") for filepath in zip_files)
    assert "Dockerrun.aws.json" in zip_files

    aws_beanstalk._clean_beanstalk_deployment(config)


def test_create_beanstalk_service(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    assert aws_beanstalk._create_beanstalk_service(config) == (
        "eb create my-service "
        "--instance_type t3.small --min-instances 1 --max-instances 1 "
        "--elb-type application --timeout 30 "
        "--vpc.id my-vpc-id --vpc.elbpublic "
        "--vpc.ec2subnets my-ec2-subnets "
        "--vpc.dbsubnets my-db-subnets "
        "--vpc.elbsubnets my-elb-subnets "
        "--envvars KEY=VARIABLE "
        "--shared-lb my-shared-load-balancer-name --shared-lb-port 443 "
        "--region us-east-2 --profile my-profile"
    )


def test_upgrade_beanstalk_instance(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    assert aws_beanstalk._upgrade_beanstalk_instance(config) == (
        "eb upgrade my-service --force --region us-east-2 --profile my-profile"
    )


def test_deploy_beanstalk_service(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    assert aws_beanstalk._deploy_beanstalk_service(config) == (
        "eb deploy my-service --region us-east-2 --profile my-profile"
    )


def test_terminate_beanstalk_service(
    beanstalk_sirtuin_config: str, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(os.path.dirname(beanstalk_sirtuin_config))

    config = aws_beanstalk._get_sirtuin_config(
        os.path.basename(beanstalk_sirtuin_config)
    )

    assert aws_beanstalk._terminate_beanstalk_service(config) == (
        "eb terminate my-service --force --region us-east-2 --profile my-profile"
    )
