from enum import Enum


class Environment(Enum):
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @staticmethod
    def get_environment(string_value: str):
        for environment in Environment:
            if environment.value.lower() == string_value.lower():
                return environment
        return None
