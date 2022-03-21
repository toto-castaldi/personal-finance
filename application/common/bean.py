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
class CoinbaseTransaction:
    id: str
    updated_at : datetime
    native_amount_amount : Decimal
    native_amount_currency : str
    type : str
    crypto_amount_amount : Decimal
    crypto_amount_currency : str

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
class PortfolioPoint:
    the_date : datetime
    assets : List[AssetAmount]
    total_amount : Decimal
    total_currency : str