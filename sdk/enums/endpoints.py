from enum import Enum


class Endpoints(Enum):
    H2H_ENDPOINT_STG = "https://checkout-stg.addonpayments.com/EPGCheckout/rest/online/pay"
    H2H_ENDPOINT_PROD = "https://checkout.addonpayments.com/EPGCheckout/rest/online/pay"
    REFUND_ENDPOINT_STG = "https://checkout-stg.addonpayments.com/EPGCheckout/rest/online/rebate"
    REFUND_ENDPOINT_PROD = "https://checkout.addonpayments.com/EPGCheckout/rest/online/rebate"
    VOID_ENDPOINT_STG = "https://checkout-stg.addonpayments.com/EPGCheckout/rest/online/void"
    VOID_ENDPOINT_PROD = "https://checkout.addonpayments.com/EPGCheckout/rest/online/void"
    CAPTURE_ENDPOINT_STG = "https://checkout-stg.addonpayments.com/EPGCheckout/rest/online/capture"
    CAPTURE_ENDPOINT_PROD = "https://checkout.addonpayments.com/EPGCheckout/rest/online/capture"
    CHARGE_ENDPOINT_STG = "https://epgjs-mep-stg.addonpayments.com/charge/v2"
    CHARGE_ENDPOINT_PROD = "https://epgjs-mep.addonpayments.com/charge/v2"
    AUTH_ENDPOINT_STG = "https://epgjs-mep-stg.addonpayments.com/auth"
    AUTH_ENDPOINT_PROD = "https://epgjs-mep.addonpayments.com/auth"
    HOSTED_ENDPOINT_STG = "https://checkout-stg.addonpayments.com/EPGCheckout/rest/online/tokenize"
    HOSTED_ENDPOINT_PROD = "https://checkout.addonpayments.com/EPGCheckout/rest/online/tokenize"
