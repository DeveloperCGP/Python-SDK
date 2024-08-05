from decimal import Decimal
from typing import Optional, Tuple

from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.quix_models.quix_flight.quix_article_flight import QuixArticleFlight
from sdk.utils.general_utils import GeneralUtils


class QuixFlightCartItem:
    __article: QuixArticleFlight = None
    __units: int = None
    __total_price_with_tax: Decimal = None
    __auto_shipping: bool = None

    def __init__(self):
        self.__units = 0
        self.__total_price_with_tax = Decimal(0.0)
        self.__auto_shipping = True

    def get_article(self) -> QuixArticleFlight:
        return self.__article

    def set_article(self, article: QuixArticleFlight) -> None:
        self.__article = article

    def get_units(self) -> int:
        return self.__units

    def set_units(self, units: int) -> None:
        self.__units = units

    def get_total_price_with_tax(self) -> Decimal:
        return self.__total_price_with_tax

    def set_total_price_with_tax(self, total_price_with_tax) -> None:
        parsed_amount = GeneralUtils.parse_amount(total_price_with_tax)
        if parsed_amount is None:
            raise InvalidFieldException(
                "total_price_with_tax: Should Follow Format #.#### And Be Between 0 And 1000000"
            )
        self.__total_price_with_tax = Decimal(parsed_amount)

    def is_auto_shipping(self) -> bool:
        return self.__auto_shipping

    def set_auto_shipping(self, auto_shipping: bool) -> None:
        self.__auto_shipping = auto_shipping

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        if self.__units <= 0:
            return True, "units"
        if self.__total_price_with_tax <= 0:
            return True, "totalPriceWithTax"
        if self.__article is None:
            return True, "article"

        return self.__article.is_missing_field()

    def to_dict(self):
        dict_with_none = {
            "units": self.__units,
            "total_price_with_tax": self.__total_price_with_tax,
            "auto_shipping": self.__auto_shipping,
            "article": self.__article,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
