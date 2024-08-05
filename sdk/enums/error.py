from enum import Enum


class Error(Enum):
    NETWORK_ERROR = "Network Error Occurred"
    INVALID_RESPONSE_RECEIVED = "Invalid Response Received"
    INVALID_AMOUNT = "Invalid Amount Received"
    MISSING_PARAMETER = "Missing Parameter"
    CLIENT_ERROR = "Client Error Occurred"
    SERVER_ERROR = "Server Error Occurred"
    INVALID_URL = "Invalid URL Provided"

    def __str__(self):
        return self.value
