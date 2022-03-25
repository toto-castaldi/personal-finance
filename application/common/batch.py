import common.utils as utils
import common.db as db
import common.fintable as fintable
import common.etherscan as etherscan
import common.blockchaincom as blockchaincom
import common.coinbase as coinbase
import common.coinapi as coinapi
import common.constants as constants
import random
import common.bean as bean
import uuid
import pytesseract
import traceback
from PIL import Image
from datetime import datetime
from datetime import timedelta
from os import listdir
from os.path import isfile, join
from decimal import Decimal


logger = utils.init_log()

def tick_job():
    logger.info("tick...")

def fintable_job():
    logger.info("fintable")
    accounts = db.load_all_accounts()
    for account in accounts:
        user_fintables = db.load_account_fintables(account)
        for user_fintable in user_fintables:
            today = datetime.today()
            balances = fintable.load_bank_account_balances(user_fintable)
            for balance in balances:
                db.save_bank_account_balance(account, today, balance[2], balance[0], balance[1])

def etherscan_job():
    logger.info("etherscan")
    accounts = db.load_all_accounts()
    for account in accounts:
        addresses = db.load_ethereum_addresses(account)
        for address in addresses:
            today = datetime.today()
            amount = etherscan.load_ethereum_amount(address)
            db.save_address_ethereum_amount(today, address, amount, None)
            rc20s = db.load_all_rc20()
            for rc20 in rc20s:
                amount = etherscan.load_rc20_amount(address, rc20.contract_address)
                db.save_address_ethereum_amount(today, address, amount, rc20.contract_address)

def blockchaincom_job():
    logger.info("blockchaincom")
    accounts = db.load_all_accounts()
    for account in accounts:
        addresses = db.load_bitcoin_addresses(account)
        for address in addresses:
            today = datetime.today()
            bitcoin_amount = blockchaincom.load_bitcoin_amount(address)
            db.save_address_bitcoin_amount(today, address, bitcoin_amount)


def coinbase_job():
    logger.info("coinbase")
    accounts = db.load_all_accounts()
    for account in accounts:
        account_transactions = coinbase.load_all_transactions(account)
        db.merge_transactions(account, account_transactions)

def coinapi_job():
    logger.info("coinapi")
    today = datetime.today().date()
    currencys_from_to = db.crypto_from_to()
    for currency_from_to in currencys_from_to:
        logger.debug(currency_from_to)
        currency_from = currency_from_to[0]
        currency_to = currency_from_to[1]
        min_date_trx, _ = db.min_max_date_trx()
        min_date_trx = min_date_trx.date()

        min_date_trx -= timedelta(days=1)
        
        logger.debug(f"{min_date_trx}")

        for single_date in utils.daterange(min_date_trx, today):
            logger.debug(single_date)
            rate = db.get_crypto_rate(single_date, currency_from, currency_to)
            if rate is None:
                rate = coinapi.rate(currency_from, currency_to, single_date)
                if rate is not None:
                    db.save_crypto_rate(single_date, currency_from, currency_to, rate)
                    logger.info(f"saved rate {single_date} {currency_from} -> {currency_to} = {rate}")

def demo_data_job():
    logger.info("demo data")
    account = db.account_info(constants.get_config()["demo_account_id"])
    logger.info("coinbase trx")
    if random.uniform(0, 1) < 2: #always
        account_transactions = [bean.CoinbaseTransaction(
            str(uuid.uuid4()),
            datetime.today(),
            random.randint(30, 500),
            "EUR",
            "buy",
            random.uniform(0, 0.003),
            random.choice(["ETH", "BTC"])
        )]
        db.merge_transactions(account, account_transactions)

def companion_images_job():
    logger.info("companion images")
    try:
        custom_oem_psm_config = r'--oem 3 --psm 6'
        upload_folder = constants.get_config()["upload_folder"]
        worked_folder = constants.get_config()["worked_folder"]
        onlyfiles = [f for f in listdir(upload_folder) if isfile(join(upload_folder, f))]
        for f in onlyfiles:
            full_path = join(upload_folder, f)
            image = Image.open(full_path)
            w, h = image.size
            footer = image.crop((0, h * (720/868), w, h ))
            #footer.save("/home/toto/tmp/abce/footer.png")

            footer_text_lines = pytesseract.image_to_string(footer, config=custom_oem_psm_config).splitlines()
            footer_last_line = footer_text_lines[-1]
            if "Negozi" in footer_last_line and "Contatti" in footer_last_line and "Servizi" in footer_last_line and "Invita" in footer_last_line and "Profilo" in footer_last_line :
                logger.info(f"{full_path} is a Satispay SCREENSHOT")

                disponibilita = image.crop((0, h * (115/868), w / 2, h * (225/868) ))
                #disponibilita.save("/home/toto/tmp/abce/disponibilita.png")

                risparmi = image.crop((w / 2, h * (115/868), w , h * (225/868) ))
                #risparmi.save("/home/toto/tmp/abce/risparmi.png")

                disponibilita_lines = pytesseract.image_to_string(disponibilita, config=custom_oem_psm_config).splitlines()
                risparmi_lines = pytesseract.image_to_string(risparmi, config=custom_oem_psm_config).splitlines()

                disponibilita_euro = Decimal(utils.str_euro_to_number(disponibilita_lines[-1]))
                risparmi_euro = Decimal(utils.str_euro_to_number(risparmi_lines[-1]))

                logger.debug(f"{disponibilita_euro} {risparmi_euro}")

                account_id = utils.account_id_from_uploaded_file(full_path)
                today = datetime.today()
                db.save_satispay(account_id, today, disponibilita_euro, risparmi_euro, "EUR", f)

                utils.move_file(full_path, worked_folder)
            else:
                logger.info(f"{full_path} is UNKNOW file ")
    except:
        traceback.print_exc()
            


