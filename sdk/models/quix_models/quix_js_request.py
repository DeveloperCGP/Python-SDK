from sdk.models.quix_models.quix_hosted_request import QuixHostedRequest


class QuixJSRequest(QuixHostedRequest):
    __prepayToken: str = None

    def __init__(self):
        super().__init__()

    def get_prepay_token(self):
        return self.__prepayToken

    def set_prepay_token(self, prepay_token):
        self.__prepayToken = prepay_token

    def is_missing_field(self):
        if not self.__prepayToken or self.__prepayToken.strip() == "":
            return True, "prepay_token"
        return super().is_missing_field()

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "prepayToken": self.__prepayToken,
        })
        return {k: v for k, v in base_dict.items() if v is not None}