import common.utils as utils
import common.db as db
import common.client.blockchaincom_client as blockchaincom_client
from datetime import datetime


logger = utils.init_log()


def blockchaincom_job():
    logger.info("blockchaincom")
    accounts = db.load_all_accounts()
    for account in accounts:
        addresses = db.load_bitcoin_addresses(account.id)
        for address in addresses:
            today = datetime.today()
            bitcoin_amount = blockchaincom_client.load_bitcoin_amount(address)
            db.save_address_bitcoin_amount(today, address, bitcoin_amount)