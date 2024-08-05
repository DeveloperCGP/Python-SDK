from typing import Optional

from sdk.exceptions.field_exception import InvalidFieldException


class Customer:

    __locale = None
    __userAgent = None
    __title = None
    __document_expiration_date = None
    __logged_in = None

    def get_locale(self) -> Optional[str]:
        return self.__locale

    def set_locale(self, locale: str) -> None:
        self.__locale = locale

    def get_user_agent(self) -> Optional[str]:
        return self.__userAgent

    def set_user_agent(self, user_agent: str) -> None:
        if len(user_agent) > 256:
            raise InvalidFieldException("userAgent: Invalid Size, Size Must Be (userAgent <= 256)")
        self.__userAgent = user_agent

    def get_title(self) -> Optional[str]:
        return self.__title

    def set_title(self, title: str) -> None:
        self.__title = title

    def get_document_expiration_date(self) -> Optional[str]:
        return self.__document_expiration_date

    def set_document_expiration_date(self, document_expiration_date: str) -> None:
        self.__document_expiration_date = document_expiration_date

    def is_logged_in(self) -> bool:
        return self.__logged_in

    def set_logged_in(self, logged_in: bool) -> None:
        self.__logged_in = logged_in

    def to_dict(self):
        dict_with_none = {
            "locale": self.__locale,
            "userAgent": self.__userAgent,
            "title": self.__title,
            "document_expiration_date": self.__document_expiration_date,
            "logged_in": self.__logged_in,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
