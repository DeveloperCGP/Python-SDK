import ipaddress
import random
import string
import urllib.parse
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import List, Tuple, Optional

import validators


class GeneralUtils:
    __RANDOM_NUMBER_SIZE: int = 44
    __amount_format: str = "0.0000"

    @staticmethod
    def round_amount(double_amount: Decimal) -> str:
        decimal_format = Decimal(double_amount).quantize(Decimal(GeneralUtils.__amount_format), rounding=ROUND_HALF_UP)
        return f"{decimal_format:f}"

    @staticmethod
    def parse_amount(amount) -> Optional[str]:
        if amount is None:
            return None
        try:
            amount = str(amount)
            if ',' in amount:
                return None
            double_amount = Decimal(amount)
            if double_amount < 0 or double_amount > 1000000:
                return None
            return GeneralUtils.round_amount(double_amount)
        except Exception as exception:
            print(exception)
            return None

    @staticmethod
    def generate_random_number():
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(GeneralUtils.__RANDOM_NUMBER_SIZE))

    @staticmethod
    def check_luhn(card_no):
        n_digits = len(card_no)
        n_sum = 0
        is_second = False

        for i in range(n_digits - 1, -1, -1):
            d = int(card_no[i])

            if is_second:
                d *= 2

            # Add digits of d (after doubling if necessary)
            n_sum += d // 10 + d % 10

            is_second = not is_second

        return n_sum % 10 == 0

    @staticmethod
    def is_valid_exp_date(exp_date):
        if exp_date is None or len(exp_date) != 4:
            return False

        month = exp_date[0:2]
        year = exp_date[2:4]

        if not month.isdigit() or not year.isdigit():
            return False

        month_int = int(month)
        year_int = int(year)

        return 1 <= month_int <= 12 and year_int >= 1

    @staticmethod
    def is_valid_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_url(url):
        return validators.url(url)

    @staticmethod
    def merchant_params_query(merchant_params: List[Tuple[str, str]]) -> str:
        merchant_params_query = []
        for parameter in merchant_params:
            merchant_params_query.append(f"{parameter[0]}:{parameter[1]}")
        return ";".join(merchant_params_query)

    @staticmethod
    def contains_null(fields) -> Tuple[bool, any]:
        for name, value in fields.items():
            if value is None:
                return True, name

        return False, None

    @staticmethod
    def get_class_attributes(cls):
        attributes = vars(cls)
        class_name = cls.__class__.__name__
        cleaned_attributes = {}

        for key, value in attributes.items():
            if key.startswith(f"_{class_name}__"):
                key = key[len(f"_{class_name}__"):]
            elif key.startswith(f"{class_name}__"):
                key = key[len(f"{class_name}__"):]
            elif key.startswith("_"):
                key = key[1:]
            cleaned_attributes[key] = value

        return cleaned_attributes

    @staticmethod
    def clean_names(cls, attributes):
        class_name = cls.__class__.__name__
        cleaned_attributes = {}

        for key, value in attributes.items():
            if key.startswith(f"_{class_name}__"):
                key = key[len(f"_{class_name}__"):]
            elif key.startswith(f"{class_name}__"):
                key = key[len(f"{class_name}__"):]
            elif key.startswith("_"):
                key = key[1:]
            cleaned_attributes[key] = value

        return cleaned_attributes

    @staticmethod
    def generate_query(cls):
        attributes = GeneralUtils.get_clean_class_attributes(cls)
        query = []

        for key, value in attributes.items():
            if value is not None:
                if isinstance(value, Enum) and value.value is not None and len(value.value) > 0:
                    query.append(f"{key}={value.value}")
                elif key == 'paySolExtendedData':
                    continue
                elif key == 'merchantParams':
                    query.append(f"{key}={GeneralUtils.merchant_params_query(value)}")
                else:
                    query.append(f"{key}={value}")

        return "&".join(query)

    @staticmethod
    def get_clean_class_attributes(cls):
        attributes = vars(cls)
        class_name = cls.__class__.__name__
        base_classes = cls.__class__.__bases__
        classes_names = [class_name] + [base_class.__name__ for base_class in base_classes]
        cleaned_attributes = {}

        for clazz_name in classes_names:
            for key, value in attributes.items():
                clean_key = None
                if key.startswith(f"_{clazz_name}__"):
                    clean_key = key[len(f"_{clazz_name}__"):]
                elif key.startswith(f"{clazz_name}__"):
                    clean_key = key[len(f"{clazz_name}__"):]

                if clean_key:
                    cleaned_attributes[clean_key] = value

        return cleaned_attributes

    @staticmethod
    def encode_url(http_query, use_safe=True):
        encoded_query = urllib.parse.quote(http_query, safe='=&;:' if use_safe else '')
        return encoded_query
