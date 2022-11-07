from enum import Enum


class AwsInstance(str, Enum):
    T3_MICRO = "t3.micro"
    T3_SMALL = "t3.small"
    T3_MEDIUM = "t3.medium"
