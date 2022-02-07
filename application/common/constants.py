import json
import os
import common.utils as utils

config = None


def get_config():
  global config
  if not config:
    if utils.is_dev_env():
        config = {
            "coinapi_key" : os.getenv("COINAPI_KEY")
        }
    else:
        with open("./common/config.json", "r") as f:
            json_file = f.read()
            config = json.loads(json_file)

  return config