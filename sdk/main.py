from sdk.enums.environment import Environment
from sdk.models.credentials import Credentials


def main():
    creds = Credentials()
    creds.set_environment(Environment.STAGING)
    creds.set_merchant_id("116659")
    creds.set_merchant_key("35354a7e-ce21-40e7-863e-e58a8e53499e")
    creds.set_merchant_pass("a723a2ce8ec3840c848d5914520c8199")
    creds.set_product_id("1166590003")
    creds.set_api_version(5)


if __name__ == "__main__":
    main()
