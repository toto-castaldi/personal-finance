import common.utils as utils
import common.db as db
import common.bean as bean
from datetime import datetime
from datetime import timedelta

logger = utils.init_log()



class Portfolio():
    def __init__(self, account):
        self.values = []
        today = datetime.today().date()
        min_trx_crypto_account, _ = db.min_max_date_trx_by_account(account)
        min_trx_crypto_account = min_trx_crypto_account.date()
        min_trx_crypto_account -= timedelta(days=1)

        logger.debug(f"{min_trx_crypto_account}")

        for down_range in utils.daterange(min_trx_crypto_account, today):
            logger.debug(down_range)
            up_range = down_range + timedelta(days=1)
            crypto_trxs = db.load_crypto_trxs_by_user_and_date(account, down_range, up_range)
            for crypto_trx in crypto_trxs:
                self.add_crypto(down_range, crypto_trx)

    def add_crypto(self, the_data, crypto_trx):
        if len(self.values) == 0:
            logger.debug(the_data, crypto_trx)
            assets = [bean.AssetAmount(
              crypto_trx.crypto_amount_amount if crypto_trx.type == "buy" else -  crypto_trx.crypto_amount_amount,
              "CRYPTO",
              crypto_trx.crypto_amount_currency
            )]
            self.values.append(bean.PortfolioPoint(
                the_data,
                assets
            ))
        else:
            pass


    def asset_points(self):
        return self.values