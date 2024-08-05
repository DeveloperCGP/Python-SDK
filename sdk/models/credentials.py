import re

from sdk.enums.environment import Environment
from sdk.exceptions.field_exception import InvalidFieldException


class Credentials:
    __merchantId: str = None
    __merchantKey: str = None
    __merchantPass: str = None
    __environment: Environment = None
    __productId: str = None
    __apiVersion: int = None

    def set_merchant_id(self, new_merchant_id: str):
        if new_merchant_id is None or not new_merchant_id.isdigit() or len(new_merchant_id) < 4 or len(new_merchant_id) > 7:
            raise InvalidFieldException("merchantId: Should be numbers in size 4 <= merchantId <= 7")
        self.__merchantId = new_merchant_id

    def get_merchant_id(self) -> str:
        return self.__merchantId

    def set_merchant_key(self, new_merchant_key: str):
        if not bool(re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$').match(new_merchant_key)):
            raise InvalidFieldException("merchantKey: Must be in UUID format")
        self.__merchantKey = new_merchant_key

    def get_merchant_key(self) -> str:
        return self.__merchantKey

    def set_merchant_pass(self, new_merchant_pass: str):
        self.__merchantPass = new_merchant_pass

    def get_merchant_pass(self) -> str:
        return self.__merchantPass

    def set_environment(self, new_environment: Environment):
        self.__environment = new_environment

    def get_environment(self) -> Environment:
        return self.__environment

    def set_product_id(self, new_product_id: str):
        if not new_product_id.isdigit() or len(new_product_id) < 6 or len(new_product_id) > 11:
            raise InvalidFieldException("productId: Should be numbers in size 6 <= productId <= 11")
        self.__productId = new_product_id

    def get_product_id(self) -> str:
        return self.__productId

    def set_api_version(self, new_api_version: int):
        if new_api_version < 0:
            raise InvalidFieldException("apiVersion: Should be (apiVersion > 0)")
        self.__apiVersion = new_api_version

    def get_api_version(self) -> int:
        return self.__apiVersion
