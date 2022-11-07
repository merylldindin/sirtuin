from enum import Enum

DEFAULT_CONFIG_FILE = 'sirtuin.toml'

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    STAGING = "staging"
    TESTING = "testing"


class Routine(str, Enum):
    CREATE_BEANSTALK = "create-beanstalk"
    DEPLOY_BEANSTALK = "deploy-beanstalk"
    DEPLOY_CLOUDFRONT = "deploy-cloudfront"
    TERMINATE_BEANSTALK = "terminate-beanstalk"
    UPGRADE_INSTANCE = "upgrade-beanstalk"
