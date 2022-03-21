import common.utils as utils
import common.db as db
import common.bean as bean
from datetime import datetime
from datetime import timedelta

logger = utils.init_log()

class Portfolio():
    def __init__(self, account):
        self.values = []
        self.account = account
        self.today = datetime.today().date()

        #self.add_public_bitcoins()
        self.coinbase()

    def coinbase(self):
        def new_date(the_data):
            prev = []
            if len(self.values) > 0:
                last_val = self.values[-1]
                prev = last_val.assets
            
            self.values.append(bean.PortfolioPoint(
                    the_data,
                    prev,
                    None,
                    None
            ))


        coinbase_min_trx_crypto_account, _ = db.min_max_coinbase_date_trx_by_account(self.account)
        min_trx_crypto_account = coinbase_min_trx_crypto_account.date()
        min_trx_crypto_account -= timedelta(days=1)
        
        logger.debug(f"{min_trx_crypto_account}")

        for down_range in utils.daterange(min_trx_crypto_account, self.today):
            logger.debug(down_range)
            new_date(down_range)
            up_range = down_range + timedelta(days=1)
            coinbase_crypto_trxs = db.load_coinbase_crypto_trxs_by_user_and_date(self.account, down_range, up_range)
                        
            for crypto_trx in coinbase_crypto_trxs:
                self.add_coinbase_crypto(down_range, crypto_trx)

    def add_coinbase_crypto(self, the_data, crypto_trx):
        def trx_amount(crypto_trx):
            if crypto_trx.type == "buy":
                return abs(crypto_trx.crypto_amount_amount)
            if crypto_trx.type == "send":
                return -abs(crypto_trx.crypto_amount_amount)
            logger.warn(f"unknow trx type {crypto_trx.type}")
            return crypto_trx.crypto_amount_amount

        def build_point(crypto_trx, prev_amount = 0, remaining_amounts = []):
            remaining_amounts.append(bean.AssetAmount(
              prev_amount + trx_amount(crypto_trx),
              "CRYPTO",
              crypto_trx.crypto_amount_currency
            ))
            return bean.PortfolioPoint(
                the_data,
                remaining_amounts,
                None,
                None
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
                total_currency = None
                total_amount = 0
                for asset in portfolio_point.assets:
                    if asset.type == "CRYPTO":
                        rate = db.get_crypto_rate(portfolio_point.the_date, asset.sub_type, native_currency )
                        if rate is not None:
                            amount = asset.amount * rate
                            converted_asset_amount = bean.ConvertedAssetAmount(
                                asset.amount,
                                asset.type,
                                asset.sub_type,
                                amount,
                                native_currency
                            )
                            total_amount += amount
                            convertes_assets.append(converted_asset_amount)
                            if total_currency is None:
                                total_currency = native_currency
                            else:
                                if total_currency != native_currency:
                                    raise ValueError(f"wrong currency : was {total_currency} now is {native_currency}")
                        else:
                            convertes_assets.append(asset)
                portfolio_point.assets = convertes_assets
                if total_currency is not None:
                    portfolio_point.total_amount = total_amount
                    portfolio_point.total_currency = total_currency
                result.append(portfolio_point)
            return result
        else:
            return self.values