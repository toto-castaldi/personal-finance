import common.utils as utils
import common.db as db
import common.constants as constants
import random
import common.bean as bean
import uuid
from datetime import datetime


logger = utils.init_log()

def demo_data_job():
    logger.info("demo data")
    account = db.account_info(constants.get_config()["demo_account_id"])
    logger.info("coinbase trx")
    if random.uniform(0, 31) <= 1: #once a month
        account_transactions = [bean.CoinbaseTransaction(
            str(uuid.uuid4()),
            datetime.today(),
            random.randint(30, 500),
            "EUR",
            "buy",
            random.uniform(0, 0.003),
            random.choice(["ETH", "BTC"])
        )]
        db.merge_transactions(account, account_transactions)           