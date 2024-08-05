from dataclasses import dataclass
from typing import Optional, Tuple

from sdk.models.quix_models.confirmation_cart_data import ConfirmationCartData
from sdk.models.quix_models.customer import Customer
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_product.quix_cart_product import QuixCartProduct
from sdk.utils.general_utils import GeneralUtils


@dataclass
class QuixItemPaySolExtendedData:
    __product: Optional[str] = None
    __disable_form_edition: bool = None
    __confirmation_card_data: ConfirmationCartData = None
    __customer: Customer = None
    __billing: QuixBilling = None
    __cart: QuixCartProduct = None

    def __init__(self):
        self.__disable_form_edition = False

    def get_confirmation_card_data(self) -> ConfirmationCartData:
        return self.__confirmation_card_data

    def set_confirmation_card_data(self, confirmation_card_data: ConfirmationCartData) -> None:
        self.__confirmation_card_data = confirmation_card_data

    def get_customer(self) -> Customer:
        return self.__customer

    def set_customer(self, customer: Customer) -> None:
        self.__customer = customer

    def get_product(self) -> Optional[str]:
        return self.__product

    def set_product(self, product: str) -> None:
        self.__product = product

    def get_billing(self) -> QuixBilling:
        return self.__billing

    def set_billing(self, billing: QuixBilling) -> None:
        self.__billing = billing

    def get_cart(self) -> QuixCartProduct:
        return self.__cart

    def set_cart(self, cart: QuixCartProduct) -> None:
        self.__cart = cart

    def is_disable_form_edition(self) -> bool:
        return self.__disable_form_edition

    def set_disable_form_edition(self, disable_form_edition: bool) -> None:
        self.__disable_form_edition = disable_form_edition

    def is_missing_field(self) -> Tuple[bool, Optional[str]]:
        mandatory_fields = {
            "product": self.__product,
            "billing": self.__billing,
            "cart": self.__cart
        }

        missing_field = GeneralUtils.contains_null(mandatory_fields)
        if missing_field[0]:
            return missing_field

        if self.__billing:
            missing_field = self.__billing.is_missing_field()
            if missing_field[0]:
                return missing_field

        if self.__cart:
            missing_field = self.__cart.is_missing_field()
            if missing_field[0]:
                return missing_field

        return False, None

    def to_dict(self):
        dict_with_none = {
            "product": self.__product,
            "disableFormEdition": self.__disable_form_edition,
            "confirmation_card_data": self.__confirmation_card_data,
            "customer": self.__customer,
            "billing": self.__billing,
            "cart": self.__cart,
        }
        return {k: v for k, v in dict_with_none.items() if v is not None}
