from decimal import Decimal
from typing import Optional, List, Tuple

from sdk.enums.currency import Currency
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.quix_models.quix_product.quix_product_cart_item import QuixProductCartItem
from sdk.utils.general_utils import GeneralUtils


class QuixCartProduct:
    __currency: Currency = None
    __total_price_with_tax: Decimal = None
    __items: List[QuixProductCartItem] = None
    __reference: Optional[str] = None

    def __init__(self):
        self.__items = []
        self.__total_price_with_tax = Decimal(0.0)

    def get_currency(self) -> Currency:
        return self.__currency

    def set_currency(self, currency: Currency) -> None:
        self.__currency = currency

    def get_total_price_with_tax(self) -> Decimal:
        return self.__total_price_with_tax

    def set_total_price_with_tax(self, total_price_with_tax) -> None:
        parsed_amount = GeneralUtils.parse_amount(total_price_with_tax)
        if parsed_amount is None:
            raise InvalidFieldException(
                "total_price_with_tax: Should Follow Format #.#### And Be Between 0 And 1000000"
            )
        self.__total_price_with_tax = Decimal(parsed_amount)

    def get_items(self) -> List[QuixProductCartItem]:
        return self.__items

    def set_items(self, items: List[QuixProductCartItem]) -> None:
        self.__items = items

    def get_reference(self) -> Optional[str]:
        return self.__reference

    def set_reference(self, reference: str) -> None:
        self.__reference = reference

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        if self.__total_price_with_tax <= 0:
            return True, "totalPriceWithTax"
        if self.__currency is None:
            return True, "currency"
        if not self.__items:
            return True, "items"

        for item in self.__items:
            missing_field = item.is_missing_field()
            if missing_field[0]:
                return missing_field

        return False, None

    def to_dict(self):
        dict_with_none = {
            "total_price_with_tax": self.__total_price_with_tax,
            "currency": self.__currency,
            "reference": self.__reference,
            "items": self.__items,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
