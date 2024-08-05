from typing import Optional, Tuple

from sdk.utils.general_utils import GeneralUtils


class QuixSegmentFlight:
    __iata_departure_code: Optional[str] = None
    __iata_destination_code: Optional[str] = None

    def get_iata_departure_code(self) -> Optional[str]:
        return self.__iata_departure_code

    def set_iata_departure_code(self, iata_departure_code: str) -> None:
        self.__iata_departure_code = iata_departure_code

    def get_iata_destination_code(self) -> Optional[str]:
        return self.__iata_destination_code

    def set_iata_destination_code(self, iata_destination_code: str) -> None:
        self.__iata_destination_code = iata_destination_code

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        mandatory_fields = {
            "iata_departure_code": self.__iata_departure_code,
            "iata_destination_code": self.__iata_destination_code
        }
        return GeneralUtils.contains_null(mandatory_fields)

    def to_dict(self):
        dict_with_none = {
            "iata_departure_code": self.__iata_departure_code,
            "iata_destination_code": self.__iata_destination_code,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
