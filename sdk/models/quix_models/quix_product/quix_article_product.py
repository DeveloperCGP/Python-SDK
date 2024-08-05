from decimal import Decimal
from typing import Optional, Tuple

from sdk.enums.category import Category
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_shipping import QuixShipping
from sdk.utils.general_utils import GeneralUtils


class QuixArticleProduct:
    """
    QuixArticleProduct
    """
    __name: Optional[str] = None
    __type: str = None
    __category: Optional[Category] = None
    __reference: Optional[str] = None
    __unit_price_with_tax: Decimal = None
    __description: Optional[str] = None
    __url: Optional[str] = None
    __image_url: Optional[str] = None
    __total_discount: Decimal = None
    __brand: Optional[str] = None
    __mpn: Optional[str] = None
    __shipping: QuixShipping = None
    __address: QuixAddress = None

    def __init__(self):
        self.__type = "product"
        self.__unit_price_with_tax = -1
        self.__total_discount = 0

    def get_name(self) -> Optional[str]:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_type(self) -> str:
        return self.__type

    def get_category(self) -> Optional[Category]:
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

    def get_description(self) -> Optional[str]:
        return self.__description

    def set_description(self, description: str) -> None:
        self.__description = description

    def get_url(self) -> Optional[str]:
        return self.__url

    def set_url(self, url: str) -> None:
        self.__url = url

    def get_image_url(self) -> Optional[str]:
        return self.__image_url

    def set_image_url(self, image_url: str) -> None:
        self.__image_url = image_url

    def get_total_discount(self) -> Decimal:
        return self.__total_discount

    def set_total_discount(self, total_discount: Decimal) -> None:
        self.__total_discount = Decimal(GeneralUtils.round_amount(total_discount))

    def get_brand(self) -> Optional[str]:
        return self.__brand

    def set_brand(self, brand: str) -> None:
        self.__brand = brand

    def get_mpn(self) -> Optional[str]:
        return self.__mpn

    def set_mpn(self, mpn: str) -> None:
        self.__mpn = mpn

    def get_shipping(self) -> QuixShipping:
        return self.__shipping

    def set_shipping(self, shipping: QuixShipping) -> None:
        self.__shipping = shipping

    def get_address(self) -> QuixAddress:
        return self.__address

    def set_address(self, address: QuixAddress) -> None:
        self.__address = address

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        if self.__unit_price_with_tax <= 0:
            return True, "unitPriceWithTax"

        mandatory_fields = {
            "name": self.__name,
            "type": self.__type,
            "category": self.__category,
            "reference": self.__reference,
        }

        return GeneralUtils.contains_null(mandatory_fields)

    def to_dict(self):
        dict_with_none = {
            "name": self.__name,
            "type": self.__type,
            "category": self.__category,
            "reference": self.__reference,
            "unit_price_with_tax": self.__unit_price_with_tax,
            "description": self.__description,
            "url": self.__url,
            "image_url": self.__image_url,
            "total_discount": self.__total_discount,
            "brand": self.__brand,
            "mpn": self.__mpn,
            "shipping": self.__shipping.to_dict() if self.__shipping else None,
            "address": self.__address.to_dict() if self.__address else None,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
