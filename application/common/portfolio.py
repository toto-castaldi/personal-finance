from tabnanny import check
import common.utils as utils
import common.db as db
import common.bean as bean
from datetime import datetime
from datetime import timedelta

logger = utils.init_log()

class Portfolio():
    def __init__(self, account, level: int = 0, node : str = None):
        self.values = []
        self.account = account
        self.today = datetime.today().date()
        self.level = level
        self.node = node

        self.dates()

        self.public_bitcoins()
        self.public_ethers()
        self.coinbase()
        self.bank_account()
        self.degiro()
        self.satispay()

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
            self.values.append(bean.PortfolioDay(
                the_date,
                []
            ))

    def check_level(self, asset_type : str, asset_subtype : str):
        if self.level == 0: return True
        if self.level == 1 and asset_type == self.node: return True
        if self.level == 2 and asset_subtype == self.node: return True
        return False


    def asset(self, porfolio_point, type, sub_type):
        assets = [x for x in porfolio_point.assets if x.type == type and x.sub_type == sub_type]
        if len(assets) == 1:
            return assets[0]
        else:
            res = bean.AssetAmount(0, type, sub_type);
            porfolio_point.assets.append(res)
            return res

    def satispay(self):
        if self.check_level("BANK", "SATISPAY"):
            for porfolio_point in self.values:
                amount = db.load_satispay_balances_at(porfolio_point.the_date, self.account)
                if amount:
                    asset_amount = self.asset(porfolio_point, "BANK", "SATISPAY")
                    asset_amount.amount += amount

    def bank_account(self):
        for porfolio_point in self.values:
            balances = db.load_bank_accout_balances_at(porfolio_point.the_date , self.account)
            for balance in balances:
                if self.check_level("BANK", balance[0]):
                    asset_amount = self.asset(porfolio_point, "BANK", balance[0])
                    asset_amount.amount += balance[1]

    def degiro(self):
        if self.check_level("INVEST", "DEGIRO"):
            for porfolio_point in self.values:
                amount = db.load_degiro_balances_at(porfolio_point.the_date, self.account)
                if amount:
                    asset_amount = self.asset(porfolio_point, "INVEST", "DEGIRO")
                    asset_amount.amount += amount

    def public_bitcoins(self):
        if self.check_level("CRYPTO", "BTC"):
            for porfolio_point in self.values:
                addresses = db.load_bitcoin_addresses(self.account)
                for address in addresses:
                    amount = db.load_public_bitcoins_amount_at(porfolio_point.the_date  + timedelta(days=1), self.account, address)
                    logger.debug(f"{porfolio_point.the_date}, {self.account}, {address} => {amount}")
                    if amount:
                        asset_amount = self.asset(porfolio_point, "CRYPTO", "BTC")
                        asset_amount.amount += amount       

    def public_ethers(self):
        for porfolio_point in self.values:
            if self.check_level("CRYPTO", "ETH"):
                amount = db.load_public_ethers_amount_at(porfolio_point.the_date + timedelta(days=1), self.account, None)
                if amount:
                    asset_amount = self.asset(porfolio_point, "CRYPTO", "ETH")
                    asset_amount.amount += amount              
            rc20s = db.load_all_rc20()
            for rc20 in rc20s:
                if self.check_level("CRYPTO", rc20.name):
                    amount = db.load_public_ethers_amount_at(porfolio_point.the_date + timedelta(days=1), self.account, rc20.contract_address)
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
                if self.check_level("CRYPTO", balance_currency):
                    asset_amount = self.asset(porfolio_point, "CRYPTO", balance_currency)
                    asset_amount.amount += balance_amount

    