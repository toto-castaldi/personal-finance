import common.utils as utils
import common.db as db
import common.client.coinbase_client as coinbase_client


logger = utils.init_log()

def coinbase_job():
    logger.info("coinbase")
    accounts = db.load_all_accounts()
    for account in accounts:
        account_transactions = coinbase_client.load_all_transactions(account)
        db.merge_transactions(account, account_transactions)