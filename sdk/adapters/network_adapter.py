from typing import Tuple, Optional

import requests

from sdk.enums.error import Error


class NetworkAdapter:

    def send_request(self, headers, query_parameters, json, url) -> Tuple[any, Optional[str]]:
        try:
            response = requests.post(url, headers=headers, params=query_parameters, json=json)
            return response.status_code, response.text
        except requests.exceptions.RequestException as e:
            print("A Network error occurred while sending the request")
            return Error.NETWORK_ERROR, str(e)
