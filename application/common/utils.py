import logging
import logging.handlers
import os

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

class ProcessnameFilter(logging.Filter):
  processName = None

  def __init__(self, processName):
    super().__init__()
    self.processName = processName 

  def filter(self, record):
    return True if self.processName in record.processName else False

def init_log():
  global logger

  if not logger:
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(log_level)
    formatter = logging.Formatter('[%(levelname)s] - %(asctime)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    f_formatter = logging.Formatter('[%(levelname)s] - %(asctime)s.%(msecs)03d: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    streamHandler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(streamHandler)

    for lf in logger_files:
      f_handler = logging.handlers.TimedRotatingFileHandler(f'./log/{lf}.log', when='midnight', backupCount=10)
      f_handler.setFormatter(f_formatter)
      f_handler.addFilter(ProcessnameFilter(lf))
      f_handler.setLevel(log_level)
      
      logger.addHandler(f_handler)

    logger.setLevel(log_level)
    
  return logger
