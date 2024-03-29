import uuid
import logging
import logging.handlers
import os
import dataclasses
import shutil
import time
from functools import wraps
from datetime import timedelta
from datetime import date
from datetime import datetime
from decimal import Decimal

LOG_LEVELS = {
  'INFO' : 20,
  'DEBUG' : 10,
  'WARNING' : 30,
  'ERROR' : 40,
  'CRITICAL' : 50
}

log_level =  LOG_LEVELS.get(os.environ.get("LOG_LEVEL","INFO"))
logger_filename = os.environ.get("LOG_FILE_NAME", None)
logger = None

EUR = "EUR"
USD = "USD"
NATIVE_CURRENCIES = [EUR, USD]
EURO_CHAR = '€'

BUYING = "buy"
COMPLETED = "completed"

PORTFOLIO_NODE_CRYPTO="CRYPTO"
PORTFOLIO_NODE_INVEST="INVEST"

PROVIDER_COINBASE = "COINBASE"
PROVIDER_MOONPAY = "MOONPAY"

def timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.debug("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result

    return wrapper

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError ("Type %s not serializable" % type(obj))


def is_dev_env():
  return os.getenv("ENV", None) == "DEV"

def init_log():
  global logger

  if not logger:
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(log_level)
    formatter = logging.Formatter('[%(levelname)s] - %(asctime)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    streamHandler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(streamHandler)

    if logger_filename is not None:
      f_handler = logging.handlers.TimedRotatingFileHandler(f'./log/{logger_filename}.log', when='midnight', backupCount=10)
      f_handler.setFormatter(formatter)
      f_handler.setLevel(log_level)
      
      logger.addHandler(f_handler)

    logger.setLevel(log_level)
    
  return logger

def daterange(start_date, end_date, step=timedelta(days=1)):
  current = start_date
  while current <= end_date:
     yield current
     current += step
  if current > end_date:
     yield end_date

def satoshi_to_bitcoin(satoshi):
  return satoshi / 100000000

def wei_to_ether(wei):
  return wei / (10 ** 18)

def str_euro_to_number(str_euro: str):
  def allowed(c):
    return str.isdigit(c) or c == '.' or c == '-'

  step0 = str_euro.replace(EURO_CHAR, '').replace('.', '').replace(',','.').strip()
  step1 = ''.join(filter(allowed, step0))

  return step1

def unique_uploaded_file_name(prefix: str, file_type: str, folder:str):
  return os.path.join(folder, f"{prefix}-upload-{uuid.uuid4()}-type-{file_type}")

#[ACCOUNT_ID]-upload-[UID]-type-image
#[ACCOUNT_ID]-upload-[UID]-type-csv
def account_id_from_uploaded_file(file_path : str):
  basename = os.path.basename(file_path)
  return basename.split("-upload-")[0]

def uuid_id_from_uploaded_file(file_path : str):
  basename = os.path.basename(file_path)
  return basename.split("-upload-")[1].split("-type-")[0]

def move_file(file, folder):
  shutil.move(file, os.path.join(folder, os.path.basename(file)))

def native_currency(raw: str):
  clean = raw.strip().upper()
  if clean in NATIVE_CURRENCIES:
    return clean
  else:
    raise ValueError(f"{clean} is an UNKNOW CURRENCY")

def crypto_currency(raw: str):
  return raw.strip().upper() #NOW WE SUPPORT EVERY CRYPTO AND TOKENS (no check)

def usd_to_eur(usd: Decimal):
  return usd * Decimal(0.95)