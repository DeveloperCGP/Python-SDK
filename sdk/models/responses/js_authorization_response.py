from sdk.enums.error import Error


class JSAuthorizationResponse:
    __authToken: str
    __isError: bool
    __error: Error
    __errorMessage: str

    def get_auth_token(self) -> str:
        return self.__authToken

    def set_auth_token(self, new_auth_token: str):
        self.__authToken = new_auth_token

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
