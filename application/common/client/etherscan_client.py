import requests
import common.utils as utils
import common.constants as constants
from decimal import Decimal

logger = utils.init_log()

apikey = constants.get_config()["etherscan_key"]

def load_ethereum_amount(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={apikey}"
    logger.debug(url)
    r = requests.get(url)
    json_response = r.json()
    logger.debug(json_response)
    if r.status_code == 200 and json_response["status"] == "1":
        logger.debug("OK")
        return utils.wei_to_ether(Decimal(json_response["result"]))
    else:
        logger.debug("KO")
        return None

def load_rc20_amount(address, contract_address):
    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest&apikey={apikey}"
    logger.debug(url)
    r = requests.get(url)
    json_response = r.json()
    logger.debug(json_response)
    if r.status_code == 200 and json_response["status"] == "1":
        logger.debug("OK")
        return utils.wei_to_ether(Decimal(json_response["result"]))
    else:
        logger.debug("KO")
        return None