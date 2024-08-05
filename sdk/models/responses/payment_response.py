from sdk.enums.error import Error
from sdk.models.responses.notification import Notification


class PaymentResponse:
    __rawResponse: str
    __isError: bool
    __error: Error
    __errorMessage: str
    __notification: Notification
    __redirectURL: str

    def get_raw_response(self) -> str:
        return self.__rawResponse

    def set_raw_response(self, new_raw_response: str):
        self.__rawResponse = new_raw_response

    def set_is_error(self, new_is_error: bool):
        self.__isError = new_is_error

    def get_is_error(self) -> bool:
        return self.__isError

    def set_error(self, new_error: Error):
        self.__error = new_error

    def get_error(self) -> Error:
        return self.__error

    def set_error_message(self, new_error_message: str):
        self.__errorMessage = new_error_message

    def get_error_message(self) -> str:
        return self.__errorMessage

    def set_notification(self, new_notification: Notification):
        self.__notification = new_notification

    def get_notification(self) -> Notification:
        return self.__notification

    def set_redirect_url(self, redirect_url: str) -> None:
        self.__redirectURL = redirect_url

    def get_redirect_url(self) -> str:
        return self.__redirectURL
