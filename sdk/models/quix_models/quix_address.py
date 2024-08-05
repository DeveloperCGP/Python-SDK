from typing import Tuple, Optional

from sdk.enums.country_code import CountryCodeAlpha3
from sdk.utils.general_utils import GeneralUtils


class QuixAddress:
    __street_address: str = None
    __street_address2: str = None
    __postalCode: str = None
    __city: str = None
    __country: CountryCodeAlpha3 = None

    def get_street_address(self) -> Optional[str]:
        return self.__street_address

    def set_street_address(self, street_address: str) -> None:
        self.__street_address = street_address

    def get_postal_code(self) -> Optional[str]:
        return self.__postalCode

    def set_postal_code(self, postal_code: str) -> None:
        self.__postalCode = postal_code

    def get_city(self) -> Optional[str]:
        return self.__city

    def set_city(self, city: str) -> None:
        self.__city = city

    def get_country(self) -> CountryCodeAlpha3:
        return self.__country

    def set_country(self, country: CountryCodeAlpha3) -> None:
        self.__country = country

    def get_street_address2(self) -> Optional[str]:
        return self.__street_address2

    def set_street_address2(self, street_address2: str) -> None:
        self.__street_address2 = street_address2

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        mandatory_fields = {
            "street_address": self.__street_address,
            "postalCode": self.__postalCode,
            "city": self.__city,
            "country": self.__country
        }
        missing_field = GeneralUtils.contains_null(mandatory_fields)
        return missing_field

    def to_dict(self):
        dict_with_none = {
            "street_address": self.__street_address,
            "street_address2": self.__street_address2,
            "postal_code": self.__postalCode,
            "city": self.__city,
            "country": self.__country,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
