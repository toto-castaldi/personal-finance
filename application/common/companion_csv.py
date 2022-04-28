import common.db as db
import common.utils as utils
import common.constants as constants
import csv
from datetime import datetime
from os import listdir
from os.path import isfile, join


logger = utils.init_log()

def job():
    logger.info("companion csv")
    
    today = datetime.today()
    upload_folder = constants.get_config()["upload_folder"]
    worked_folder = constants.get_config()["worked_folder"]
    onlyfiles = [f for f in listdir(upload_folder) if isfile(join(upload_folder, f)) and "-type-csv" in f]
    
    for f in onlyfiles:
        full_path = join(upload_folder, f)
        account_id = utils.account_id_from_uploaded_file(full_path)
        logger.debug(full_path)
        with open(full_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            csv_type = None
            for row in csv_reader:
                if line_count == 0:
                    header_csv = ",".join(row)
                    if header_csv == "Data,Ora,Prodotto,ISIN,Borsa di,Borsa,Quantità,Quotazione,,Valore locale,,Valore,,Tasso di,Commissioni di,,Totale,,ID Ordine":
                        csv_type = "DEGIRO-TRANSASCTIONS"
                    if header_csv == "Data,Ora,Data Valore,Prodotto,ISIN,Descrizione,Borsa,Variazioni,,Saldo,,ID Ordine":
                        csv_type = "DEGIRO-ACCOUNT"
                    if header_csv == '"id","operation","baseCurrency","baseCurrencyAmount","createdAt","quoteCurrency","quoteCurrencyAmount","feeAmount","extraFeeAmount","networkFeeAmount","status"':
                        csv_type = "MOONPAY-TRX"
                else:
                    if csv_type == "DEGIRO-TRANSASCTIONS":
                        db.save_degiro_transaction(account_id, today, row)
                    if csv_type == "MOONPAY-TRX":
                        db.save_moonpay_transaction(account_id, today, row)
                    if csv_type == "DEGIRO-ACCOUNT":
                        if row[5] == "Deposito flatex":
                            db.save_degiro_deposit(account_id, today, row)
                line_count += 1
            if csv_type:
                utils.move_file(full_path, worked_folder)
            
        