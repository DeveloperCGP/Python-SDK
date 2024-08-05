import urllib.parse
from typing import Optional


class ConfirmationCartData:
    __url: Optional[str] = None

    def get_url(self) -> Optional[str]:
        return self.__url

    def set_url(self, url: Optional[str]) -> None:
        if url and url.strip():
            self.__url = urllib.parse.quote(url, safe='')
        else:
            self.__url = None

    def to_dict(self):
        dict_with_none = {
            "url": self.__url,

        }
        return {k: v for k, v in dict_with_none.items() if v is not None}