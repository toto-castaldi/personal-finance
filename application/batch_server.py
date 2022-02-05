import time
import os
import schedule
import common.utils as utils
import common.db as db
import common.coinbase as coinbase
import common.coinapi as coinapi
from datetime import datetime


logger = utils.init_log()

def tick_job():
    logger.info("tick...")

def coinbase_job():
    logger.info("coinbase")
    accounts = db.load_all_accounts()
    for account in accounts:
        account_transactions = coinbase.load_all_transactions(account)
        db.merge_transactions(account, account_transactions)

def coinapi_job():
    logger.info("coinapi")
    currencys_from_to = db.coinbase_currency_from_to()
    for currency_from_to in currencys_from_to:
        logger.debug(currency_from_to)
        min_date_trx, _ = db.min_max_date_trx()
        logger.debug(f"{min_date_trx}")
        for single_date in utils.daterange(min_date_trx, datetime.today()):
            logger.debug(single_date)
            rate = coinapi.rate(currency_from_to[0], currency_from_to[1], single_date)
            db.save_crypto_rate(single_date, currency_from_to[0], currency_from_to[1], rate)


if os.getenv("ENV", None) == "DEV":
    #coinbase_job()
    coinapi_job()
else:
    db.connection_param["host"] = "postgresql"
    if __name__ == '__main__':
        schedule.every().hour.do(tick_job)
        schedule.every().day.at("10:30").do(coinbase_job)

        #schedule.every(10).seconds.do(tick_job)
        #schedule.every(10).minutes.do(tick_job)
        #schedule.every(5).to(10).minutes.do(tick_job)
        #schedule.every().monday.do(tick_job)
        #schedule.every().wednesday.at("13:15").do(tick_job)
        #schedule.every().minute.at(":17").do(tick_job)

        while True:
            schedule.run_pending()
            time.sleep(1)