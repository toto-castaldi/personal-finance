import common.utils as utils
import common.portfolio as portfolio
import json
from fastapi import Response
from fastapi import FastAPI

app = FastAPI()
logger = utils.init_log()


@app.get("/portfolio-values/{account_id}")
def portfolio_values(account_id: str):
    asset_points = portfolio.Portfolio(account_id).asset_points()
    return Response(content=json.dumps(asset_points, default=utils.json_serial), media_type="application/json")

