from locale import currency
import common.utils as utils
import common.db as db
import common.portfolio as portfolio
import json
from fastapi import Response
from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()
logger = utils.init_log()


@app.get("/portfolio-values/{account_id}/{currency}")
def portfolio_values(account_id: str, currency: str):
    logger.debug(account_id)
    if db.account_info(account_id):
        asset_points = portfolio.Portfolio(account_id).asset_points(native_currency=currency)
        return Response(content=json.dumps(asset_points, default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

