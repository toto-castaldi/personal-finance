import common.utils as utils
import common.portfolio as portfolio
from fastapi import FastAPI

app = FastAPI()
logger = utils.init_log()


@app.get("/portfolio-values/{account_id}")
def portfolio_values(account_id: str):
    logger.debug(portfolio.Portfolio(account_id).asset_points())
    return {"Hello": "World"}

