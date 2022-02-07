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
    today = datetime.today().date()
    currencys_from_to = db.coinbase_currency_from_to()
    for currency_from_to in currencys_from_to:
        logger.debug(currency_from_to)
        currency_from = currency_from_to[0]
        currency_to = currency_from_to[1]
        min_date_trx, _ = db.min_max_date_trx()
        min_date_trx = min_date_trx.date()
        
        logger.debug(f"{min_date_trx}")

        for single_date in utils.daterange(min_date_trx, today):
            logger.debug(single_date)
            rate = db.get_crypto_rate(single_date, currency_from, currency_to)
            if rate is None:
                rate = coinapi.rate(currency_from, currency_to, single_date)
                if rate is not None:
                    db.save_crypto_rate(single_date, currency_from, currency_to, rate)
                    logger.info(f"saved rate {single_date} {currency_from} -> {currency_to} = {rate}")
                    if utils.is_dev_env():
                        #just one execution
                        return


if utils.is_dev_env():
    coinbase_job()
    coinapi_job()
else:
    db.connection_param["host"] = "postgresql"
    if __name__ == '__main__':
        schedule.every().hour.do(tick_job)
        schedule.every().day.at("10:30").do(coinbase_job)
        schedule.every().day.at("12:30").do(coinapi_job)

        #schedule.every(10).seconds.do(tick_job)
        #schedule.every(10).minutes.do(tick_job)
        #schedule.every(5).to(10).minutes.do(tick_job)
        #schedule.every().monday.do(tick_job)
        #schedule.every().wednesday.at("13:15").do(tick_job)
        #schedule.every().minute.at(":17").do(tick_job)

        while True:
            schedule.run_pending()
            time.sleep(1)