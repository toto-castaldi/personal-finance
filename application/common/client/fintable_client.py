import requests
import common.utils as utils
from requests.auth import AuthBase
from decimal import Decimal


logger = utils.init_log()

class FintableAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers.update({
            "Authorization": f"Bearer {self.token}"
        })

        return request

def load_bank_account_balances(user_fintable):
    auth = FintableAuth(user_fintable.api_key)
    url = f"https://api.airtable.com/v0/{user_fintable.base_name}/Accounts?maxRecords=1&view=Grid"
    logger.debug(url)
    r = requests.get(url, auth=auth)
    json_response = r.json()
    logger.debug(json_response)
    if r.status_code == 200:
        logger.debug("OK")
        result = []
        for bank in json_response["records"]:
            logger.debug(bank)
            result.append((Decimal(bank["fields"]["**EUR"]),"EUR",bank["fields"]["*Name"]))
        return result
    else:
        logger.debug("KO")
        return None