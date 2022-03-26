import common.utils as utils
import common.db as db
import common.client.coinapi_client as coinapi_client
from datetime import datetime
from datetime import timedelta


logger = utils.init_log()

def coinapi_job():
    logger.info("coinapi")
    today = datetime.today().date()
    currencys_from_to = db.crypto_from_to()
    for currency_from_to in currencys_from_to:
        logger.debug(currency_from_to)
        currency_from = currency_from_to[0]
        currency_to = currency_from_to[1]
        min_date_trx, _ = db.min_max_date_trx()
        min_date_trx = min_date_trx.date()

        min_date_trx -= timedelta(days=1)
        
        logger.debug(f"{min_date_trx}")

        for single_date in utils.daterange(min_date_trx, today):
            logger.debug(single_date)
            rate = db.get_crypto_rate(single_date, currency_from, currency_to)
            if rate is None:
                rate = coinapi_client.rate(currency_from, currency_to, single_date)
                if rate is not None:
                    db.save_crypto_rate(single_date, currency_from, currency_to, rate)
                    logger.info(f"saved rate {single_date} {currency_from} -> {currency_to} = {rate}")