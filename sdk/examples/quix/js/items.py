from typing import List

from sdk.adapters.js_quix_payment_adapter import JSQuixPaymentAdapter
from sdk.enums.category import Category
from sdk.enums.country_code import CountryCodeAlpha3
from sdk.enums.currency import Currency
from sdk.enums.environment import Environment
from sdk.exceptions.field_exception import FieldException
from sdk.models.credentials import Credentials
from sdk.models.quix_models.quix_address import QuixAddress
from sdk.models.quix_models.quix_billing import QuixBilling
from sdk.models.quix_models.quix_product.quix_article_product import QuixArticleProduct
from sdk.models.quix_models.quix_product.quix_cart_product import QuixCartProduct
from sdk.models.quix_models.quix_product.quix_item_pay_sol_extended_data import QuixItemPaySolExtendedData
from sdk.models.quix_models.quix_product.quix_product_cart_item import QuixProductCartItem
from sdk.models.requests.quix_js.js_quix_item import JSQuixItem
from sdk.utils import creds


class QuixJSItems:

    @staticmethod
    def send_quix_js_items():
        try:
            # Step 1 - Creating Credentials Object
            credentials = Credentials()
            credentials.set_environment(
                Environment.STAGING if creds.environment.lower() == "staging".lower() else Environment.PRODUCTION
            )
            credentials.set_merchant_id(creds.merchant_id)
            credentials.set_merchant_key(creds.merchant_key)
            credentials.set_merchant_pass(creds.merchant_pass)
            credentials.set_product_id(creds.product_id_item)
            credentials.set_api_version(int(creds.api_version))

            # Step 2 - Configure Payment Parameters
            request = JSQuixItem()
            request.set_prepay_token("55354a9e-c121-41e7-863e-e58a7653499e")
            request.set_amount("99")
            request.set_customer_id("903")
            request.set_status_url(creds.status_url)
            request.set_success_url(creds.success_url)
            request.set_error_url(creds.error_url)
            request.set_awaiting_url(creds.awaiting_url)
            request.set_cancel_url(creds.cancel_url)
            request.set_customer_email("test@mail.com")
            request.set_customer_national_id("99999999R")
            request.set_dob("01-12-1999")
            request.set_first_name("Name")
            request.set_last_name("Last Name")
            request.set_ip_address("0.0.0.0")

            quix_article_product = QuixArticleProduct()
            quix_article_product.set_name("Nombre del servicio 2")
            quix_article_product.set_reference("4912345678903")
            quix_article_product.set_unit_price_with_tax(99)
            quix_article_product.set_category(Category.DIGITAL)

            quix_item_cart_item_product = QuixProductCartItem()
            quix_item_cart_item_product.set_article(quix_article_product)
            quix_item_cart_item_product.set_units(1)
            quix_item_cart_item_product.set_auto_shipping(True)
            quix_item_cart_item_product.set_total_price_with_tax(99)

            # Create items list and add quixItemCartItemProduct
            items: List[QuixProductCartItem] = [quix_item_cart_item_product]

            # Create QuixCartProduct and set its attributes using setters
            quix_cart_product = QuixCartProduct()
            quix_cart_product.set_currency(Currency.EUR)
            quix_cart_product.set_items(items)
            quix_cart_product.set_total_price_with_tax('99')

            # Create QuixAddress and set its attributes using setters
            quix_address = QuixAddress()
            quix_address.set_city("Barcelona")
            quix_address.set_country(CountryCodeAlpha3.ESP)
            quix_address.set_street_address("Nombre de la vía y nº")
            quix_address.set_postal_code("28003")

            # Create QuixBilling and set its attributes using setters
            quix_billing = QuixBilling()
            quix_billing.set_address(quix_address)
            quix_billing.set_first_name("Nombre")
            quix_billing.set_last_name("Apellido")

            # Create QuixItemPaySolExtendedData and set its attributes using setters
            quix_item_pay_sol_extended_data = QuixItemPaySolExtendedData()
            quix_item_pay_sol_extended_data.set_cart(quix_cart_product)
            quix_item_pay_sol_extended_data.set_billing(quix_billing)
            quix_item_pay_sol_extended_data.set_product("instalments")

            # Set paySolExtendedData for hostedQuixItem using setter
            request.set_pay_sol_extended_data(quix_item_pay_sol_extended_data)

            result = JSQuixPaymentAdapter(credentials).send_js_quix_item_request(request)
            print(f"nemuru_cart_hash: {result.get_notification().get_nemuru_cart_hash()}")
            print(f"nemuru_auth_token: {result.get_notification().get_nemuru_auth_token()}")
        except FieldException as field_exception:
            print(field_exception)


if __name__ == "__main__":
    QuixJSItems.send_quix_js_items()
