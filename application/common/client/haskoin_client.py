import requests
import common.utils as utils
from decimal import Decimal

logger = utils.init_log()

def load_bitcoin_amount(xpub):
    url = f"https://api.haskoin.com/btc/xpub/{xpub}?derive=segwit"
    logger.debug(url)
    r = requests.get(url)
    json_response = r.json()
    logger.debug(json_response)
    if r.status_code == 200:
        logger.debug("OK")
        return utils.satoshi_to_bitcoin(Decimal(json_response["balance"]["confirmed"]))
    else:
        logger.debug("KO")
        return None