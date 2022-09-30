import common.db as db


def buying(account_id: str, currency: str):
    result = {}
    degiro_deposits = db.load_degiro_deposits_by_user(account_id)
    result["movements"] = [];
    result["total_amount"] = 0;
    result["total_currency"] = currency;
    for movement in degiro_deposits:
        result["movements"].append(movement)
        result["total_amount"] += movement.amount
    def sort_updated_at(e):
            return e.updated_at

    result["movements"].sort(key=sort_updated_at)

    return result