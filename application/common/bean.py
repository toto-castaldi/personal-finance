from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List


@dataclass
class Account:
    id: str
    coinbase_api_key: str
    coinbase_api_secret: str

@dataclass
class RC20:
    name: str
    contract_address: str

@dataclass
class FintableAccount:
    base_name: str
    api_key: str

@dataclass
class CoinbaseTransaction:
    id: str
    updated_at : datetime
    native_amount_amount : Decimal
    native_amount_currency : str
    type : str
    crypto_amount_amount : Decimal
    crypto_amount_currency : str

@dataclass
class DegiroDeposit:
    updated_at : datetime
    amount : Decimal
    currency : str

@dataclass
class CryptoTransaction:
    id: str
    native_amount_amount : Decimal
    updated_at : datetime
    crypto_amount_amount : Decimal
    provider : str
    crypto_amount_currency: str
    native_amount_currency : str


@dataclass
class MoonpayTransaction:
    id: str
    type : str
    native_amount_amount : Decimal
    native_amount_currency : str
    updated_at : datetime
    crypto_amount_amount : Decimal
    crypto_amount_currency : str
    fee_amount : Decimal
    extrafee_amount : Decimal
    networkfee_amount : Decimal
    status : Decimal

@dataclass
class AssetAmount:
    amount : Decimal
    type : str
    sub_type : str

@dataclass
class ConvertedAssetAmount(AssetAmount):
    native_amount : Decimal
    native_currency : str


@dataclass
class PortfolioDay:
    the_date : datetime
    assets : List[AssetAmount]