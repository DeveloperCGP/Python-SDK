import json

from sdk.adapters.hosted_quix_payment_adapter import HostedQuixPaymentAdapter
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.quix_models.quix_accommodation.auix_accommodation_cart_item import QuixAccommodationCartItem
from sdk.models.quix_models.quix_accommodation.auix_article_accommodation import QuixArticleAccommodation
from sdk.models.quix_models.quix_accommodation.quix_accommodation_pay_sol_extended_data import \
    QuixAccommodationPaySolExtendedData
from sdk.models.quix_models.quix_accommodation.quix_cart_accommodation import QuixCartAccommodation
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.requests.quix_hosted.hosted_quix_accommodation import HostedQuixAccommodation
from sdk.utils import creds
from sdk.utils.custom_encoder import CustomEncoder


class QuixHostedAccommodationService:

    @staticmethod
    def send_quix_hosted_accommodation_request():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_environment(
                Environment.STAGING if creds.environment.lower() == "staging".lower() else Environment.PRODUCTION
            )
            credentials.set_merchant_id(creds.merchant_id)
            credentials.set_merchant_pass(creds.merchant_pass)
            credentials.set_product_id(creds.product_id_accommodation)
            credentials.set_api_version(int(creds.api_version))

            # Step 2 - Configure Payment Parameters
            request = HostedQuixAccommodation()
            request.set_amount("99")
            request.set_customer_id("903")
            request.set_status_url(creds.status_url)
            request.set_success_url(creds.success_url)
            request.set_error_url(creds.error_url)
            request.set_awaiting_url(creds.awaiting_url)
            request.set_cancel_url(creds.cancel_url)
            request.set_customer_email("test@mail.com")
            request.set_dob("01-12-1999")
            request.set_customer_national_id("99999999R")
            request.set_first_name("Name")
            request.set_last_name("Last Name")
            request.set_ip_address("0.0.0.0")

            quix_address = QuixAddress()
            quix_address.set_city("Barcelona")
            quix_address.set_country(CountryCodeAlpha3.ESP)
            quix_address.set_street_address("Nombre de la vía y nº")
            quix_address.set_postal_code("28003")

            quix_article_accommodation = QuixArticleAccommodation()
            quix_article_accommodation.set_name("Nombre del servicio 2")
            quix_article_accommodation.set_reference("4912345678903")
            quix_article_accommodation.set_checkin_date("2024-10-30T00:00:00+01:00")
            quix_article_accommodation.set_checkout_date("2024-12-31T23:59:59+01:00")
            quix_article_accommodation.set_guests(1)
            quix_article_accommodation.set_establishment_name("Hotel")
            quix_article_accommodation.set_address(quix_address)
            quix_article_accommodation.set_unit_price_with_tax(99)
            quix_article_accommodation.set_category(Category.DIGITAL)

            quix_item_cart_item_accommodation = QuixAccommodationCartItem()
            quix_item_cart_item_accommodation.set_article(quix_article_accommodation)
            quix_item_cart_item_accommodation.set_units(1)
            quix_item_cart_item_accommodation.set_auto_shipping(True)
            quix_item_cart_item_accommodation.set_total_price_with_tax(99)

            items = [quix_item_cart_item_accommodation]

            quix_cart_accommodation = QuixCartAccommodation()
            quix_cart_accommodation.set_currency(Currency.EUR)
            quix_cart_accommodation.set_items(items)
            quix_cart_accommodation.set_total_price_with_tax(99)

            quix_billing = QuixBilling()
            quix_billing.set_address(quix_address)
            quix_billing.set_first_name("Nombre")
            quix_billing.set_last_name("Apellido")

            quix_accommodation_pay_sol_extended_data = QuixAccommodationPaySolExtendedData()
            quix_accommodation_pay_sol_extended_data.set_cart(quix_cart_accommodation)
            quix_accommodation_pay_sol_extended_data.set_billing(quix_billing)
            quix_accommodation_pay_sol_extended_data.set_product("instalments")

            request.set_pay_sol_extended_data(quix_accommodation_pay_sol_extended_data)
            print(json.dumps(request, cls=CustomEncoder))
            # Step 3 - Send Payment Request
            result = HostedQuixPaymentAdapter(credentials).send_hosted_quix_accommodation_request(request)
            print(result.get_notification().get_redirect_url())
        except FieldException as field_exception:
            print(field_exception)


if __name__ == "__main__":
    QuixHostedAccommodationService.send_quix_hosted_accommodation_request()
