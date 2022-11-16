import common.utils as utils
import common.db as db
import common.constants as constants
import pytesseract
import traceback
from PIL import Image
from datetime import datetime
from os import listdir
from os.path import isfile, join
from decimal import Decimal

logger = utils.init_log()
debug_counter = 0
custom_oem_psm_config = r'--oem 3 --psm 6'

def extract_footer_last_lines(image, start_y_ratio, end_x_ratio = None, end_y_ratio = None):
    global debug_counter
    w, h = image.size
    y_end = h if end_y_ratio is None else h * end_y_ratio
    w_end = w if end_x_ratio is None else w * end_x_ratio
    cropped = image.crop((0, h * start_y_ratio, w_end, y_end ))
    if utils.is_dev_env():
        debug_counter = debug_counter + 1
        cropped.save(f"cropped-debug-{debug_counter}.png")
    footer_text_lines = pytesseract.image_to_string(cropped, config=custom_oem_psm_config).splitlines()
    return footer_text_lines

def image_type(full_path):
    image = Image.open(full_path)
    footer_last_lines = extract_footer_last_lines(image, 720/868)
    for footer_last_line in footer_last_lines:
        if "Negozi" in footer_last_line and "Contatti" in footer_last_line and "Servizi" in footer_last_line and "Invita" in footer_last_line and "Profilo" in footer_last_line :
            return image, "SATISPAY"
            
    footer_last_lines = footer_last_line = extract_footer_last_lines(image, 760/868)
    for footer_last_line in footer_last_lines:
        logger.debug(footer_last_line)
        if "Mercato" in footer_last_line and "Preferiti" in footer_last_line and "Portafoglio" in footer_last_line :
            return image, "DEGIRO"
    
    footer_last_lines = footer_last_line = extract_footer_last_lines(image, 795/868, 0.5, 815/868)
    for footer_last_line in footer_last_lines:
        if "Mercato" in footer_last_line and "Preferiti" in footer_last_line :
            return image, "DEGIRO"

    logger.warning("UNKNOW image....")

    return image, None

def image_value_satispay(image):
    w, h = image.size

    disponibilita = image.crop((0, h * (115/868), w / 2, h * (225/868) ))

    risparmi = image.crop((w / 2, h * (115/868), w , h * (225/868) ))

    disponibilita_lines = pytesseract.image_to_string(disponibilita, config=custom_oem_psm_config).splitlines()
    risparmi_lines = pytesseract.image_to_string(risparmi, config=custom_oem_psm_config).splitlines()

    logger.debug(disponibilita_lines)
    logger.debug(risparmi_lines)

    disponibilita_euro = None
    risparmi_euro = None

    for line in disponibilita_lines:
        if len(line) > 0 and line[0].isdigit():
            disponibilita_euro = Decimal(utils.str_euro_to_number(line))

    for line in risparmi_lines:
        if len(line) > 0 and line[0].isdigit():
            risparmi_euro = Decimal(utils.str_euro_to_number(line))

    logger.debug(f"{disponibilita_euro} {risparmi_euro}")

    return disponibilita_euro, risparmi_euro

def image_value_degiro(image):
    global debug_counter
    w, h = image.size

    width =  w / 2 - w * (6/400)

    amount_tesseract_lines = ["INVALID"]
    

    while amount_tesseract_lines[0][0] != utils.EURO_CHAR and width > 0:

        bank_amount_image = image.crop((w * (40/400), h * (27/868), width, h * (59/868) ))

        if utils.is_dev_env():
            debug_counter = debug_counter + 1
            bank_amount_image.save(f"cropped-debug-{debug_counter}.png")

        amount_tesseract_lines = pytesseract.image_to_string(bank_amount_image, config=custom_oem_psm_config).splitlines();

        logger.debug(amount_tesseract_lines)

        width = width + 1;

    bank_amount = Decimal(utils.str_euro_to_number(amount_tesseract_lines[0]))
    logger.debug(bank_amount)
    return bank_amount

def job():
    logger.info("companion images")
    try:
        today = datetime.today()
        
        upload_folder = constants.get_config()["upload_folder"]
        worked_folder = constants.get_config()["worked_folder"]
        unknow_folder = constants.get_config()["unknow_folder"]
        error_folder = constants.get_config()["error_folder"]
        onlyfiles = [f for f in listdir(upload_folder) if isfile(join(upload_folder, f)) and "-type-image" in f]
        
        for f in onlyfiles:
            full_path = join(upload_folder, f)
            account_id = utils.account_id_from_uploaded_file(full_path)

            image, image_type_ = image_type(full_path)

            if image_type_ == "SATISPAY" :
                try:
                    logger.info(f"{full_path} is a Satispay SCREENSHOT")

                    disponibilita_euro, risparmi_euro = image_value_satispay(image)
                    
                    db.save_satispay(account_id, today, disponibilita_euro, risparmi_euro, "EUR", f)
                    utils.move_file(full_path, worked_folder)
                except:
                    logger.error("exception ",exc_info=1)
                    utils.move_file(full_path, error_folder)

            if image_type_ == "DEGIRO" :
                try:
                    logger.info(f"{full_path} is a Degiro SCREENSHOT")
                    
                    degiro_value = image_value_degiro(image)

                    db.save_degiro_balance(account_id, today, degiro_value, "EUR", f)
                    utils.move_file(full_path, worked_folder)
                except:
                    logger.error("exception ",exc_info=1)
                    utils.move_file(full_path, error_folder)

            if image_type_ is None:
                logger.info(f"{full_path} is UNKNOW file ")
                utils.move_file(full_path, unknow_folder)
    except:
        traceback.print_exc()
        logger.error("exception ",exc_info=1)