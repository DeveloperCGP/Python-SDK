from enum import Enum


class ResponseCodes(Enum):
    MIN_SUCCESS = 200
    MAX_SUCCESS = 299
    REDIRECTION = 307
    MIN_CLIENT_ERROR = 400
    MAX_CLIENT_ERROR = 499

    @staticmethod
    def is_success(status_code) -> bool:
        if (ResponseCodes.MIN_SUCCESS.value <= status_code <= ResponseCodes.MAX_SUCCESS.value) or status_code == ResponseCodes.REDIRECTION.value:
            return True
        else:
            return False

    @staticmethod
    def is_client_error(status_code) -> bool:
        if ResponseCodes.MIN_CLIENT_ERROR.value <= status_code <= ResponseCodes.MAX_CLIENT_ERROR.value:
            return True
        else:
            return False
