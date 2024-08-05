from typing import Optional, Tuple

from sdk.models.quix_models.quix_js_request import QuixJSRequest
from sdk.models.quix_models.quix_service.quix_service_pay_sol_extended_data import QuixServicePaySolExtendedData


class JSQuixService(QuixJSRequest):
    __paySolExtendedData: Optional[QuixServicePaySolExtendedData] = None

    def __init__(self):
        super().__init__()

    def get_pay_sol_extended_data(self) -> Optional[QuixServicePaySolExtendedData]:
        return self.__paySolExtendedData

    def set_pay_sol_extended_data(self, pay_sol_extended_data: QuixServicePaySolExtendedData) -> None:
        self.__paySolExtendedData = pay_sol_extended_data

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        if self.__paySolExtendedData is None:
            return True, "paySolExtendedData"

        missing_field = self.__paySolExtendedData.is_missing_field()
        if missing_field[0]:
            return missing_field

        return super().is_missing_field()

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "paysolExtendedData": self.__paySolExtendedData.to_dict() if self.__paySolExtendedData else None,
        })
        return {k: v for k, v in base_dict.items() if v is not None}
