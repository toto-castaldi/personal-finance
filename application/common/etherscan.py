import common.utils as utils
import common.db as db
import common.client.etherscan_client as etherscan_client
from datetime import datetime


logger = utils.init_log()

def etherscan_job():
    logger.info("etherscan")
    accounts = db.load_all_accounts()
    for account in accounts:
        addresses = db.load_ethereum_addresses(account)
        for address in addresses:
            today = datetime.today()
            amount = etherscan_client.load_ethereum_amount(address)
            db.save_address_ethereum_amount(today, address, amount, None)
            rc20s = db.load_all_rc20()
            for rc20 in rc20s:
                amount = etherscan_client.load_rc20_amount(address, rc20.contract_address)
                db.save_address_ethereum_amount(today, address, amount, rc20.contract_address)