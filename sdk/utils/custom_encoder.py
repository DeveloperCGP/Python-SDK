import json
from decimal import Decimal
from enum import Enum


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif isinstance(obj, Enum) and obj is not None:
            return obj.value
        elif isinstance(obj, Decimal) and obj is not None:
            return float(obj)
        return super().default(obj)
