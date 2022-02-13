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
            self.new_date(down_range)
            up_range = down_range + timedelta(days=1)
            crypto_trxs = db.load_crypto_trxs_by_user_and_date(account, down_range, up_range)
            
            for crypto_trx in crypto_trxs:
                self.add_crypto(down_range, crypto_trx)

    def new_date(self, the_data):
        prev = []
        if len(self.values) > 0:
            last_val = self.values[-1]
            prev = last_val.assets
        
        self.values.append(bean.PortfolioPoint(
                the_data,
                prev
        ))

    def add_crypto(self, the_data, crypto_trx):
        def build_point(crypto_trx, prev_amount = 0, remaining_amounts = []):
            remaining_amounts.append(bean.AssetAmount(
              prev_amount + ( crypto_trx.crypto_amount_amount if crypto_trx.type == "buy" else -  crypto_trx.crypto_amount_amount),
              "CRYPTO",
              crypto_trx.crypto_amount_currency
            ))
            return bean.PortfolioPoint(
                the_data,
                remaining_amounts
            )

        last_val = self.values[-1]
        prev_amounts = [x for x in last_val.assets if x.type == "CRYPTO" and x.sub_type == crypto_trx.crypto_amount_currency]
        remaining_amounts = [x for x in last_val.assets if x.type != "CRYPTO" or x.sub_type != crypto_trx.crypto_amount_currency]
        if len(prev_amounts) == 0:
            self.values[-1] = build_point(crypto_trx, 0, remaining_amounts)
        elif len(prev_amounts) == 1:
            self.values[-1] = build_point(crypto_trx, prev_amounts[0].amount, remaining_amounts)
        else:
            raise ValueError("too many values")


    def asset_points(self, native_currency = None):
        if native_currency:

            result = []
            for portfolio_point in self.values:
                convertes_assets = []
                for asset in portfolio_point.assets:
                    if asset.type == "CRYPTO":
                        rate = db.get_crypto_rate(portfolio_point.the_date, asset.sub_type, native_currency )
                        if rate is not None:
                            converted_asset_amount = bean.ConvertedAssetAmount(
                                asset.amount,
                                asset.type,
                                asset.sub_type,
                                asset.amount * rate,
                                native_currency
                            )
                            convertes_assets.append(converted_asset_amount)
                        else:
                            convertes_assets.append(asset)
                portfolio_point.assets = convertes_assets
                result.append(portfolio_point)
            return result
        else:
            return self.values