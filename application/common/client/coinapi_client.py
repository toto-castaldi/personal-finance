import requests
import common.utils as utils
import common.constants as constants
from requests.auth import AuthBase


logger = utils.init_log()

class CoinApiAuth(AuthBase):
    def __init__(self, coinbase_token):
        self.coinbase_token = coinbase_token

    def __call__(self, request):
        request.headers.update({
            "X-CoinAPI-Key": self.coinbase_token
        })

        return request

def rate(currency_from, currency_to, date):
    auth = CoinApiAuth(constants.get_config()["coinapi_key"])
    str_time = date.isoformat()#strftime("%yyyy-%mm-%dd")
    url = f"https://rest.coinapi.io/v1/exchangerate/{currency_from}/{currency_to}?time={str_time}"
    logger.debug(url)
    r = requests.get(url, auth=auth)
    json_response = r.json()
    logger.debug(json_response)
    if r.status_code == 200:
        logger.debug("OK")
        return json_response["rate"]
    else:
        logger.debug("KO")
        return None