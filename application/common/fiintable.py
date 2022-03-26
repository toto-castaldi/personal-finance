import common.utils as utils
import common.db as db
import common.client.fintable_client as fintable_client
import common.bean as bean
from datetime import datetime

logger = utils.init_log()

def fintable_job():
    logger.info("fintable")
    accounts = db.load_all_accounts()
    for account in accounts:
        user_fintables = db.load_account_fintables(account)
        for user_fintable in user_fintables:
            today = datetime.today()
            balances = fintable_client.load_bank_account_balances(user_fintable)
            for balance in balances:
                db.save_bank_account_balance(account.id, today, balance[2], balance[0], balance[1])