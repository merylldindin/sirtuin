from argparse import ArgumentParser, Namespace

from controllers import deploy_controller, support_controller

from sirtuin.models.routines import DevopsScript, Environment


def _get_arguments() -> Namespace:
    parser = ArgumentParser(description="Control shell scripts")
    parser.add_argument("-s", "--script", type=DevopsScript)
    parser.add_argument("-m", "--mode", type=Environment)

    return parser.parse_args()


arguments = _get_arguments()

if arguments.script == DevopsScript.CREATE_BEANSTALK:
    deploy_controller.create_beanstalk_service(arguments.mode)

if arguments.script == DevopsScript.DEPLOY_BEANSTALK:
    deploy_controller.deploy_beanstalk_service(arguments.mode)

if arguments.script == DevopsScript.DEPLOY_CLOUDFRONT:
    deploy_controller.sync_s3_bucket(arguments.mode)

if arguments.script == DevopsScript.UPGRADE_INSTANCE:
    support_controller.upgrade_beanstalk_instance(arguments.mode)

if arguments.script == DevopsScript.END_SERVICE:
    deploy_controller.terminate_beanstalk_service(arguments.mode)
