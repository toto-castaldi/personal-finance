import common.utils as utils
import common.db as db
import common.constants as constants
import common.bean as bean
import pytesseract
import traceback
from PIL import Image
from datetime import datetime
from os import listdir
from os.path import isfile, join
from decimal import Decimal

logger = utils.init_log()


def images_job():
    def extract_footer_last_line(image, start_y_ratio):
        w, h = image.size
        footer = image.crop((0, h * start_y_ratio, w, h ))
        #footer.save("/home/toto/tmp/abce/footer.png")
        footer_text_lines = pytesseract.image_to_string(footer, config=custom_oem_psm_config).splitlines()
        return footer_text_lines[-1]

    logger.info("companion images")
    try:
        today = datetime.today()
        custom_oem_psm_config = r'--oem 3 --psm 6'
        upload_folder = constants.get_config()["upload_folder"]
        worked_folder = constants.get_config()["worked_folder"]
        onlyfiles = [f for f in listdir(upload_folder) if isfile(join(upload_folder, f))]
        
        for f in onlyfiles:
            full_path = join(upload_folder, f)
            account_id = utils.account_id_from_uploaded_file(full_path)
            image = Image.open(full_path)
            w, h = image.size
            image_type = None

            footer_last_line = extract_footer_last_line(image, 720/868)
            if "Negozi" in footer_last_line and "Contatti" in footer_last_line and "Servizi" in footer_last_line and "Invita" in footer_last_line and "Profilo" in footer_last_line :
                image_type = "SATISPAY"
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
                
                db.save_satispay(account_id, today, disponibilita_euro, risparmi_euro, "EUR", f)

                utils.move_file(full_path, worked_folder)

            footer_last_line = footer_last_line = extract_footer_last_line(image, 760/868)
            if "Mercato" in footer_last_line and "Preferiti" in footer_last_line and "Portafoglio" in footer_last_line and "Attivita" in footer_last_line :
                image_type = "DEGIRO"
                logger.info(f"{full_path} is a Degiro SCREENSHOT")
                bank_amount_image = image.crop((w * (40/400), h * (25/868), w / 2 - w * (10/400), h * (59/868) ))
                #bank_amount_image.save("/home/toto/tmp/abce/bank_amount.png")

                bank_amount = Decimal(utils.str_euro_to_number(pytesseract.image_to_string(bank_amount_image, config=custom_oem_psm_config).splitlines()[0]))
                logger.debug(bank_amount)

                db.save_bank_account_balance(account_id, today, "Degiro", bank_amount, "EUR", f)

            if not image_type:
                logger.info(f"{full_path} is UNKNOW file ")
    except:
        traceback.print_exc()