import uvicorn
import common.utils as utils
import common.db as db

if __name__ == "__main__":
  if utils.is_dev_env():
    uvicorn.run("api.routes:app", host='0.0.0.0', port=5000, reload=True, workers=1)
  else:
    uvicorn.run("api.routes:app", host='0.0.0.0', port=5000, workers=4)