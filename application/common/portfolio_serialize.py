import common.db as db
import common.bean as bean
import common.portfolio as p


def asset_points(porfolio : p.Portfolio, native_currency = None):
    if native_currency:

        result = []
        for portfolio_point in porfolio.values:
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
        return porfolio.values