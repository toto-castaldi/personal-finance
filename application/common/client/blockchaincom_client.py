import requests
import common.utils as utils
from decimal import Decimal

logger = utils.init_log()

def load_bitcoin_amount(address):
    url = f"https://blockchain.info/q/addressbalance/{address}?confirmations=3"
    logger.debug(url)
    r = requests.get(url)
    text_response = r.content.decode('UTF-8')
    logger.debug(text_response)
    if r.status_code == 200:
        logger.debug("OK")
        return utils.satoshi_to_bitcoin(Decimal(text_response.strip()))
    else:
        logger.debug("KO")
        return None