from typing import Tuple

from sdk.models.requests.h2h.h2h_redirection import H2HRedirection


class H2HPreAuthorization(H2HRedirection):

    def __init__(self):
        super().__init__()
        self.set_auto_capture(False)

    def is_missing_field(self) -> Tuple[bool, any]:
        if self.get_auto_capture() is None:
            return True, "autoCapture"
        return super().is_missing_field()
