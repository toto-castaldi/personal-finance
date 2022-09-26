import common.db as db
import common.bean as bean
import common.utils as utils



def buying(account_id: str, currency: str):
    result = {}
    coinbase_movements = db.load_coinbase_crypto_trxs_by_user(account_id)
    moonpay_movements = db.load_moonpay_crypto_trxs_by_user(account_id)
    result["movements"] = [];
    result["total_amount"] = 0;
    result["total_currency"] = currency;
    for movement in coinbase_movements:
        if movement.type == utils.BUYING:
            if movement.native_amount_currency != currency:
                if movement.native_amount_currency == utils.USD:
                    movement.native_amount_amount = utils.usd_to_eur(movement.native_amount_amount)
                else:
                    ValueError(f"{movement.native_amount_currency} is an UNKNOW CURRENCY")
            m = bean.CryptoTransaction(
                movement.id,
                movement.native_amount_amount,
                movement.updated_at, 
                movement.crypto_amount_amount,
                utils.PROVIDER_COINBASE,
                movement.crypto_amount_currency,
                movement.native_amount_currency

            )
            result["movements"].append(m)
            result["total_amount"] += m.native_amount_amount
    for movement in moonpay_movements:
        if movement.type == utils.BUYING and movement.status == utils.COMPLETED:
            if movement.native_amount_currency != currency:
                if movement.native_amount_currency == utils.USD:
                    movement.native_amount_amount = utils.usd_to_eur(movement.native_amount_amount)
                    movement.fee_amount = utils.usd_to_eur(movement.fee_amount)
                    movement.extrafee_amount = utils.usd_to_eur(movement.extrafee_amount)
                    movement.networkfee_amount = utils.usd_to_eur(movement.fee_amount)
                    movement.native_amount_currency = utils.EUR
                else:
                    ValueError(f"{movement.native_amount_currency} is an UNKNOW CURRENCY")
            m = bean.CryptoTransaction(
                movement.id,
                movement.native_amount_amount + movement.fee_amount + movement.extrafee_amount + movement.networkfee_amount,
                movement.updated_at, 
                movement.crypto_amount_amount,
                utils.PROVIDER_MOONPAY,
                movement.crypto_amount_currency,
                movement.native_amount_currency
            )
            
            result["movements"].append(m)
            result["total_amount"] += m.native_amount_amount
    def sort_updated_at(e):
            return e.updated_at

    result["movements"].sort(key=sort_updated_at)

    return result