from typing import Tuple, Optional

from sdk.models.quix_models.quix_address import QuixAddress
from sdk.utils.general_utils import GeneralUtils


class QuixBilling:
    __first_name = None
    __last_name = None
    __address = None
    __corporate_id_number = None

    def get_first_name(self) -> str:
        return self.__first_name

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def set_last_name(self, last_name: str) -> None:
        self.__last_name = last_name

    def get_address(self) -> QuixAddress:
        return self.__address

    def set_address(self, address: QuixAddress) -> None:
        self.__address = address

    def get_corporate_id_number(self) -> Optional[str]:
        return self.__corporate_id_number

    def set_corporate_id_number(self, corporate_id_number: Optional[str]) -> None:
        self.__corporate_id_number = corporate_id_number

    def is_missing_field(self) -> Tuple[bool, str]:
        mandatory_fields = {"first_name": self.__first_name,
                            "last_name": self.__last_name,
                            "address": self.__address}
        missing_field = GeneralUtils.contains_null(mandatory_fields)
        if missing_field[0]:
            return missing_field

        return self.__address.is_missing_field()

    def to_dict(self):
        dict_with_none = {
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "address": self.__address,
            "corporate_id_number": self.__corporate_id_number,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
