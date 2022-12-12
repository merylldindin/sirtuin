from enum import Enum


class LoadBalancerType(str, Enum):
    APPLICATION = "application"
    CLASSIC = "classic"
    NETWORK = "network"
