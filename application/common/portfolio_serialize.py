from tkinter.messagebox import NO
import common.db as db
import common.bean as bean
import common.portfolio as p
import common.utils as utils
from dataclasses import dataclass
from decimal import Decimal

logger = utils.init_log()

@dataclass
class PortfolioAmount(bean.PortfolioDay):
    total_amount : Decimal
    total_currency : str

def add_amount_to_point(portfolio_point : bean.PortfolioDay, native_currency : str):
    convertes_assets = []
    total_currency = None
    total_amount = 0
    converted_asset_amount = None
    the_date = portfolio_point.the_date
    for asset in portfolio_point.assets:
        amount = 0
        if asset.type == "CRYPTO":
            rate = db.get_crypto_rate(the_date, asset.sub_type, native_currency )
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

    
    pp = PortfolioAmount(the_date, convertes_assets, None, None)
    if total_currency is not None:
        pp.total_amount = total_amount
        pp.total_currency = total_currency

    return pp

def summary(porfolio : p.Portfolio, native_currency = None):
    if native_currency and len(porfolio.values) > 0:
        logger.debug(porfolio.values[-1])
        return add_amount_to_point(porfolio.values[-1], native_currency)

    else:
        return None


def asset_points(portfolio : p.Portfolio, native_currency : str, max_num_of_points : int ):
    assert native_currency is not None
    assert max_num_of_points is not None and max_num_of_points > 2
    assert portfolio is not None

    result = []
    len_vals = len(portfolio.values)
    if len_vals <= max_num_of_points:
        for portfolio_point in portfolio.values:
            result.append(add_amount_to_point(portfolio_point, native_currency))
    else:
        max_num_of_points -= 2
        step = len_vals / max_num_of_points
        index = 0
        while index < len_vals:
            result.append(add_amount_to_point(portfolio.values[index], native_currency))
            index = int(index + step)

        result.append(add_amount_to_point(portfolio.values[-1], native_currency))

    return result
    