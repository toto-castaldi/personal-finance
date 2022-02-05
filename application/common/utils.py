import logging
import logging.handlers
import os
from datetime import timedelta

LOG_LEVELS = {
  'INFO' : 20,
  'DEBUG' : 10,
  'WARNING' : 30,
  'ERROR' : 40,
  'CRITICAL' : 50
}

log_level =  LOG_LEVELS.get(os.environ.get('LOG_LEVEL','INFO'))
logger_files = ['batch']
logger = None


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

    for lf in logger_files:
      f_handler = logging.handlers.TimedRotatingFileHandler(f'./log/{lf}.log', when='midnight', backupCount=10)
      f_handler.setFormatter(formatter)
      f_handler.setLevel(log_level)
      
      logger.addHandler(f_handler)

    logger.setLevel(log_level)
    
  return logger

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)
