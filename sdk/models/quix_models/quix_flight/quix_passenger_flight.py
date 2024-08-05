from typing import Optional, Tuple

from sdk.utils.general_utils import GeneralUtils


class QuixPassengerFlight:
    __first_name: Optional[str] = None
    __last_name: Optional[str] = None

    def get_first_name(self) -> Optional[str]:
        return self.__first_name

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = first_name

    def get_last_name(self) -> Optional[str]:
        return self.__last_name

    def set_last_name(self, last_name: str) -> None:
        self.__last_name = last_name

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        mandatory_fields = {
            "first_name": self.__first_name,
            "last_name": self.__last_name
        }
        return GeneralUtils.contains_null(mandatory_fields)

    def to_dict(self):
        dict_with_none = {
            "first_name": self.__first_name,
            "last_name": self.__last_name,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
