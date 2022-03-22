import common.utils as utils
import common.db as db
import common.portfolio as portfolio
import common.portfolio_serialize as portfolio_serialize
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
        return Response(content=json.dumps(portfolio_serialize.asset_points(portfolio.Portfolio(account_id), native_currency=currency), default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/portfolio-summary/{account_id}/{currency}")
def portfolio_values_json(account_id: str, currency: str):
    if db.account_info(account_id):
        return Response(content=json.dumps(portfolio_serialize.summary(portfolio.Portfolio(account_id), native_currency=currency), default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")