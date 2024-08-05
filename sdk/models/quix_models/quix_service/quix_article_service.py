import urllib.parse
from decimal import Decimal
from typing import Optional, Tuple

from sdk.enums.category import Category
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.utils.general_utils import GeneralUtils


class QuixArticleService:
    __name: Optional[str] = None
    __type: str = "service"
    __start_date: Optional[str] = None
    __end_date: Optional[str] = None
    __category: Category = None
    __reference: Optional[str] = None
    __unit_price_with_tax: Decimal = None
    __description: Optional[str] = None
    __url: Optional[str] = None
    __image_url: Optional[str] = None
    __total_discount: Decimal = None

    def __init__(self):
        self.__type = "service"
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

    def get_start_date(self) -> Optional[str]:
        return self.__start_date

    def set_start_date(self, start_date: str) -> None:
        self.__start_date = start_date

    def get_end_date(self) -> Optional[str]:
        return self.__end_date

    def set_end_date(self, end_date: str) -> None:
        self.__end_date = end_date

    def get_description(self) -> Optional[str]:
        return self.__description

    def set_description(self, description: str) -> None:
        self.__description = description

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

    def set_total_discount(self, total_discount: Decimal) -> None:
        if total_discount < 0:
            raise InvalidFieldException("totalDiscount: Value must be (totalDiscount >= 0)")
        self.__total_discount = Decimal(GeneralUtils.round_amount(total_discount))

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        if self.__unit_price_with_tax <= 0:
            return True, "unitPriceWithTax"
        mandatory_fields = {
            "name": self.__name,
            "type": self.__type,
            "category": self.__category,
            "reference": self.__reference,
            "end_date": self.__end_date
        }
        return GeneralUtils.contains_null(mandatory_fields)

    def to_dict(self):
        dict_with_none = {
            "name": self.__name,
            "type": self.__type,
            "start_date": self.__start_date,
            "end_date": self.__end_date,
            "category": self.__category,
            "reference": self.__reference,
            "unit_price_with_tax": self.__unit_price_with_tax,
            "description": self.__description,
            "url": self.__url,
            "image_url": self.__image_url,
            "total_discount": self.__total_discount,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
