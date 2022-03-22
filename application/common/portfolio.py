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

        self.dates()

        self.public_bitcoins()
        self.public_ethers()
        self.coinbase()
        self.bank_account()

    def dates(self):
        bitcoin_min_date, _ = db.min_max_public_bitcoins_date_trx_by_account(self.account)
        coinbase_min_date, _ = db.min_max_coinbase_date_trx_by_account(self.account)
        bank_min_date, _ = db.min_max_bank_by_account(self.account)


        min_date = min(
            bitcoin_min_date if bitcoin_min_date else datetime.today(), 
            coinbase_min_date if coinbase_min_date else datetime.today(),
            bank_min_date if bank_min_date else datetime.today(),
        )
        min_date = min_date.date()
        for the_date in utils.daterange(min_date, self.today):
            logger.debug(the_date)
            self.values.append(bean.PortfolioPoint(
                the_date,
                [],
                None,
                None
            ))

    def asset(self, porfolio_point, type, sub_type):
        assets = [x for x in porfolio_point.assets if x.type == type and x.sub_type == sub_type]
        if len(assets) == 1:
            return assets[0]
        else:
            res = bean.AssetAmount(0, type, sub_type);
            porfolio_point.assets.append(res)
            return res

    def bank_account(self):
        for porfolio_point in self.values:
            balances = db.load_bank_accout_balances_at(porfolio_point.the_date, self.account)
            for balance in balances:
                asset_amount = self.asset(porfolio_point, "BANK", balance[0])
                asset_amount.amount += balance[1]

    def public_bitcoins(self):
        for porfolio_point in self.values:
            amount = db.load_public_bitcoins_amount_at(porfolio_point.the_date, self.account)
            if amount:
                asset_amount = self.asset(porfolio_point, "CRYPTO", "BTC")
                asset_amount.amount += amount       

    def public_ethers(self):
        for porfolio_point in self.values:
            amount = db.load_public_ethers_amount_at(porfolio_point.the_date, self.account, None)
            if amount:
                asset_amount = self.asset(porfolio_point, "CRYPTO", "ETH")
                asset_amount.amount += amount              
            rc20s = db.load_all_rc20()
            for rc20 in rc20s:
                amount = db.load_public_ethers_amount_at(porfolio_point.the_date, self.account, rc20.contract_address)
                if amount:
                    asset_amount = self.asset(porfolio_point, "CRYPTO", rc20.name)
                    asset_amount.amount += amount
            
            
    def coinbase(self):
        def trx_amount(crypto_trx):
            if crypto_trx.type == "buy":
                return abs(crypto_trx.crypto_amount_amount)
            if crypto_trx.type == "send":
                return -abs(crypto_trx.crypto_amount_amount)
            logger.warn(f"unknow trx type {crypto_trx.type}")
            return crypto_trx.crypto_amount_amount

        coinbase_balance = {}

        for porfolio_point in self.values:
            up_range = porfolio_point.the_date + timedelta(days=1)
            coinbase_crypto_trxs = db.load_coinbase_crypto_trxs_by_user_and_date(self.account, porfolio_point.the_date, up_range)
                        
            for crypto_trx in coinbase_crypto_trxs:
                prev_amount = coinbase_balance[crypto_trx.crypto_amount_currency] if crypto_trx.crypto_amount_currency in coinbase_balance else 0
                coinbase_balance[crypto_trx.crypto_amount_currency] = prev_amount + trx_amount(crypto_trx)

            for balance_currency, balance_amount in coinbase_balance.items():
                asset_amount = self.asset(porfolio_point, "CRYPTO", balance_currency)
                asset_amount.amount += balance_amount

    def asset_points(self, native_currency = None):
        if native_currency:

            result = []
            for portfolio_point in self.values:
                convertes_assets = []
                total_currency = None
                total_amount = 0
                converted_asset_amount = None
                for asset in portfolio_point.assets:
                    amount = 0
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
                            convertes_assets.append(converted_asset_amount)

                        else:
                            convertes_assets.append(asset)
                    elif asset.type == "BANK":
                        amount = asset.amount 
                        converted_asset_amount = bean.ConvertedAssetAmount(
                                asset.amount,
                                asset.type,
                                asset.sub_type,
                                amount,
                                "EUR"
                        )
                        convertes_assets.append(converted_asset_amount)
                    
                    total_amount += amount
                    if total_currency is None:
                                total_currency = native_currency
                    else:
                        if total_currency != native_currency:
                            raise ValueError(f"wrong currency : was {total_currency} now is {native_currency}")

                portfolio_point.assets = convertes_assets
                if total_currency is not None:
                    portfolio_point.total_amount = total_amount
                    portfolio_point.total_currency = total_currency
                result.append(portfolio_point)
            return result
        else:
            return self.values