from enum import Enum


class Method(Enum):
    HOME = "home"
    DIGITAL = "digital"
    POSTAL = "postal"
    PICK_UP_POINT = "pick_up_point"
    PICK_UP_STORE = "pick_up_store"
    PICK_UP_WAREHOUSE = "pick_up_warehouse"
    OWN = "own"
    CLICK_COLLECT = "click_collect"
