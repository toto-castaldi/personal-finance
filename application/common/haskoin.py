import common.utils as utils
import common.db as db
import common.client.haskoin_client as haskoin_client
from datetime import datetime


logger = utils.init_log()


def job():
    logger.info("haskoin")
    accounts = db.load_all_accounts()
    for account in accounts:
        addresses = db.load_bitcoin_addresses(account.id)
        for address in addresses:
            logger.debug(address)
            if address.startswith("xpub"):
                today = datetime.today()
                bitcoin_amount = haskoin_client.load_bitcoin_amount(address)
                db.save_address_bitcoin_amount(today, address, bitcoin_amount)