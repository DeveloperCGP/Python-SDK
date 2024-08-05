import urllib.parse
from decimal import Decimal
from typing import Optional, Tuple

from sdk.enums.category import Category
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.utils.general_utils import GeneralUtils


class QuixArticleAccommodation:
    __name: Optional[str] = None
    __type: str = None
    __category: Category = None
    __reference: Optional[str] = None
    __unit_price_with_tax: Decimal = None
    __checkin_date: Optional[str] = None
    __checkout_date: Optional[str] = None
    __establishment_name: Optional[str] = None
    __address: QuixAddress = None
    __guests: int = None
    __url: Optional[str] = None
    __image_url: Optional[str] = None
    __total_discount: Decimal = 0

    def __init__(self):
        self.__type = "accommodation"
        self.__guests = -1
        self.__unit_price_with_tax = -1
        self.__total_discount = 0

    def get_name(self) -> Optional[str]:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_type(self) -> str:
        return self.__type

    def get_category(self) -> Category:
        return self.__category

    def set_category(self, category: Category) -> None:
        self.__category = category

    def get_reference(self) -> Optional[str]:
        return self.__reference

    def set_reference(self, reference: str) -> None:
        self.__reference = reference

    def get_unit_price_with_tax(self) -> Decimal:
        return self.__unit_price_with_tax

    def set_unit_price_with_tax(self, unit_price_with_tax) -> None:
        parsed_amount = GeneralUtils.parse_amount(unit_price_with_tax)
        if parsed_amount is None:
            raise InvalidFieldException(
                "unit_price_with_tax: Should Follow Format #.#### And Be Between 0 And 1000000"
            )
        self.__unit_price_with_tax = Decimal(parsed_amount)

    def get_checkin_date(self) -> Optional[str]:
        return self.__checkin_date

    def set_checkin_date(self, checkin_date: str) -> None:
        self.__checkin_date = checkin_date

    def get_checkout_date(self) -> Optional[str]:
        return self.__checkout_date

    def set_checkout_date(self, checkout_date: str) -> None:
        self.__checkout_date = checkout_date

    def get_establishment_name(self) -> Optional[str]:
        return self.__establishment_name

    def set_establishment_name(self, establishment_name: str) -> None:
        self.__establishment_name = establishment_name

    def get_address(self) -> QuixAddress:
        return self.__address

    def set_address(self, address: QuixAddress) -> None:
        self.__address = address

    def get_guests(self) -> int:
        return self.__guests

    def set_guests(self, guests: int) -> None:
        self.__guests = guests

    def get_url(self) -> Optional[str]:
        return self.__url

    def set_url(self, url: str) -> None:
        if url and url.strip():
            self.__url = urllib.parse.quote(url, safe='')
        else:
            self.__url = None

    def get_image_url(self) -> Optional[str]:
        return self.__image_url

    def set_image_url(self, image_url: str) -> None:
        if image_url and image_url.strip():
            self.__image_url = urllib.parse.quote(image_url, safe='')
        else:
            self.__image_url = None

    def get_total_discount(self) -> Decimal:
        return self.__total_discount

    def set_total_discount(self, total_discount) -> None:
        parsed_amount = GeneralUtils.parse_amount(total_discount)
        if parsed_amount is None:
            raise InvalidFieldException(
                "total_discount: Should Follow Format #.#### And Be Between 0 And 1000000"
            )
        self.__total_discount = Decimal(parsed_amount)

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        if self.__unit_price_with_tax <= 0:
            return True, "unitPriceWithTax"
        if self.__guests <= 0:
            return True, "guests"

        mandatory_fields = {
            "name": self.__name,
            "type": self.__type,
            "category": self.__category,
            "reference": self.__reference,
            "checkin_date": self.__checkin_date,
            "checkout_date": self.__checkout_date,
            "establishment_name": self.__establishment_name,
            "address": self.__address,
            "guests": self.__guests
        }
        missing_field = GeneralUtils.contains_null(mandatory_fields)
        if missing_field[0]:
            return missing_field

        return self.__address.is_missing_field()

    def to_dict(self):
        dict_with_none = {
            "name": self.__name,
            "type": self.__type,
            "category": self.__category,
            "reference": self.__reference,
            "unit_price_with_tax": self.__unit_price_with_tax,
            "checkin_date": self.__checkin_date,
            "checkout_date": self.__checkout_date,
            "establishment_name": self.__establishment_name,
            "address": self.__address.to_dict() if self.__address else None,
            "guests": self.__guests,
            "url": self.__url,
            "image_url": self.__image_url,
            "total_discount": self.__total_discount,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
