from typing import Optional

from sdk.enums.method import Method
from sdk.models.quix_models.quix_address import QuixAddress


class QuixShipping:
    __name: str = None
    __first_name: str = None
    __last_name: str = None
    __company: str = None
    __email: str = None
    __phone_number: str = None
    __method: Method = None
    __address: QuixAddress = None

    def get_name(self) -> Optional[str]:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_first_name(self) -> Optional[str]:
        return self.__first_name

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = first_name

    def get_last_name(self) -> Optional[str]:
        return self.__last_name

    def set_last_name(self, last_name: str) -> None:
        self.__last_name = last_name

    def get_company(self) -> Optional[str]:
        return self.__company

    def set_company(self, company: str) -> None:
        self.__company = company

    def get_email(self) -> Optional[str]:
        return self.__email

    def set_email(self, email: str) -> None:
        self.__email = email

    def get_phone_number(self) -> Optional[str]:
        return self.__phone_number

    def set_phone_number(self, phone_number: str) -> None:
        self.__phone_number = phone_number

    def get_method(self) -> Method:
        return self.__method

    def set_method(self, method: Method) -> None:
        self.__method = method

    def get_address(self) -> QuixAddress:
        return self.__address

    def set_address(self, address: QuixAddress) -> None:
        self.__address = address

    def to_dict(self):
        dict_with_none = {
            "name": self.__name,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "company": self.__company,
            "email": self.__email,
            "phone_number": self.__phone_number,
            "method": self.__method.value if self.__method else None,
            "address": self.__address,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
