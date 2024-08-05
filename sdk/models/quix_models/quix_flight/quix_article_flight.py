from decimal import Decimal
from typing import Optional, List, Tuple

from sdk.enums.category import Category
from sdk.exceptions.field_exception import InvalidFieldException
from sdk.models.quix_models.quix_flight.quix_passenger_flight import QuixPassengerFlight
from sdk.models.quix_models.quix_flight.quix_segment_flight import QuixSegmentFlight
from sdk.utils.general_utils import GeneralUtils


class QuixArticleFlight:
    __name: Optional[str] = None
    __type: str = None
    __category: Category = None
    __reference: Optional[str] = None
    __unit_price_with_tax: Decimal = None
    __departure_date: Optional[str] = None
    __passengers: List[QuixPassengerFlight] = None
    __segments: List[QuixSegmentFlight] = None

    def __init__(self):
        self.__type = "flight"
        self.__unit_price_with_tax = Decimal(-1)

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
            raise InvalidFieldException("unit_price_with_tax: Should Follow Format #.#### And Be Between 0 And 1000000")
        self.__unit_price_with_tax = Decimal(parsed_amount)

    def get_departure_date(self) -> Optional[str]:
        return self.__departure_date

    def set_departure_date(self, departure_date: str) -> None:
        self.__departure_date = departure_date

    def get_passengers(self) -> List[QuixPassengerFlight]:
        return self.__passengers

    def set_passengers(self, passengers: List[QuixPassengerFlight]) -> None:
        self.__passengers = passengers

    def get_segments(self) -> List[QuixSegmentFlight]:
        return self.__segments

    def set_segments(self, segments: List[QuixSegmentFlight]) -> None:
        self.__segments = segments

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        if self.__unit_price_with_tax <= 0:
            return True, "unitPriceWithTax"

        mandatory_fields = {
            "name": self.__name,
            "type": self.__type,
            "category": self.__category,
            "reference": self.__reference,
            "departure_date": self.__departure_date,
            "passengers": self.__passengers,
            "segments": self.__segments
        }

        missing_field = GeneralUtils.contains_null(mandatory_fields)
        if missing_field[0]:
            return missing_field

        if not self.__passengers:
            return True, "passengers"
        if not self.__segments:
            return True, "segments"

        for item in self.__passengers:
            missing_field = item.is_missing_field()
            if missing_field[0]:
                return missing_field

        for item in self.__segments:
            missing_field = item.is_missing_field()
            if missing_field[0]:
                return missing_field

        return False, None

    def to_dict(self):
        dict_with_none = {
            "name": self.__name,
            "type": self.__type,
            "category": self.__category,
            "reference": self.__reference,
            "unit_price_with_tax": self.__unit_price_with_tax,
            "departure_date": self.__departure_date,
            "passengers": [passenger.to_dict() for passenger in self.__passengers] if self.__passengers else None,
            "segments": [segment.to_dict() for segment in self.__segments] if self.__segments else None,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}