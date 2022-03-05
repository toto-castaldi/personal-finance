from locale import currency
import common.utils as utils
import common.db as db
import common.portfolio as portfolio
import common.bean as bean
import json
from fastapi import Response
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = utils.init_log()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/portfolio-values/{account_id}/{currency}")
def portfolio_values_json(account_id: str, currency: str):
    logger.debug(account_id)
    if db.account_info(account_id):
        asset_points = portfolio.Portfolio(account_id).asset_points(native_currency=currency)
        return Response(content=json.dumps(asset_points, default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/portfolio-values-csv/{account_id}/{currency}")
def portfolio_values_csv(account_id: str, currency: str):
    logger.debug(account_id)
    if db.account_info(account_id):
        asset_points = portfolio.Portfolio(account_id).asset_points(native_currency=currency)
        headers = {"Content-Disposition": "attachment;filename=portfolio.csv"}
        res = "DATE, AMOUNT" 
        for ap in asset_points:
            res += "\n" + f"{ap.the_date},{ap.total_amount}"
        return Response(content=res, media_type="text/csv", headers=headers)
    else:
        raise HTTPException(status_code=404, detail="wrong account")

