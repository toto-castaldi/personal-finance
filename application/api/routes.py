from decimal import Decimal
import common.utils as utils
import common.db as db
import common.portfolio as portfolio
import common.portfolio_serialize as portfolio_serialize
import common.constants as constants
import common.crypto as crypto
import common.invest as invest
import json
from datetime import datetime
from fastapi import Response
from fastapi import FastAPI, Form
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = utils.init_log()

origins = [
    "*"
]

upload_folder = constants.get_config()["upload_folder"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/file/")
async def file(uploaded_file = Form(...), uid:str = Form(...), type:str = Form(...)):
    contents = await uploaded_file.read()
    filename = utils.unique_uploaded_file_name(uid, type, upload_folder)

    logger.info(f"{filename} uploaded")

    with open(filename, "wb") as f:
        f.write(contents)

    return filename

@app.get("/portfolio-values/{account_id}/{level}/{node}/{currency}/{max_num_of_points}")
def portfolio_values_json(account_id: str, level: int, node : str, currency: str, max_num_of_points : int):
    logger.debug(account_id)
    if db.account_info(account_id):
        p = portfolio.Portfolio(account_id, level, node)
        return Response(content=json.dumps(
            portfolio_serialize.asset_points(
                p, 
                currency,
                max_num_of_points
            ), 
            default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/portfolio-summary/{account_id}/{level}/{node}/{currency}")
def portfolio_values_json(account_id: str, level: int, node : str, currency: str):
    if db.account_info(account_id):
        p = portfolio.Portfolio(account_id, level, node)

        return Response(content=json.dumps(portfolio_serialize.summary(p, native_currency=currency), default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/portfolio-level/{account_id}/{level}/{node}")
def portfolio_level(account_id: str, level: int, node : str):
    if db.account_info(account_id):
        nodes = portfolio_serialize.level(portfolio.Portfolio(account_id), level, node);
        return Response(content=json.dumps(nodes, default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/crypto-apr/{account_id}/{currency}")
def crypto_apr(account_id: str, currency: str):
    if db.account_info(account_id):
        total_crypto = portfolio_serialize.summary(portfolio.Portfolio(account_id, 1, utils.PORTFOLIO_NODE_CRYPTO), native_currency=currency)
        buying = crypto.buying(account_id, currency)

        actual_value = total_crypto.total_amount
        buying_value = buying["total_amount"]

        days = (datetime.today() - buying["movements"][0].updated_at).days
        apr = 100 * ((actual_value/buying_value-1)/Decimal(days/365))
        delta = actual_value - buying_value

        return Response(content=json.dumps({ "apr" : apr, "delta" : delta, "native_amount_currency" : currency}, default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/investment-apr/{account_id}/{currency}")
def investment_apr(account_id: str, currency: str):
    if db.account_info(account_id):
        total_invest = portfolio_serialize.summary(portfolio.Portfolio(account_id, 1, utils.PORTFOLIO_NODE_INVEST), native_currency=currency)
        buying = invest.buying(account_id, currency)

        actual_value = total_invest.total_amount
        buying_value = buying["total_amount"]

        days = (datetime.today() - buying["movements"][0].updated_at).days
        apr = 100 * ((actual_value/buying_value-1)/Decimal(days/365))
        delta = actual_value - buying_value

        return Response(content=json.dumps({ "apr" : apr, "delta" : delta, "native_amount_currency" : currency}, default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/crypto-buying/{account_id}/{currency}")
def crypto_buing(account_id: str, currency: str):
    if currency != utils.EUR:
        raise HTTPException(status_code=404, detail="we support only EUR")
    if db.account_info(account_id):
        result = crypto.buying(account_id, currency)

        return Response(content=json.dumps(result, default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/investment-deposit/{account_id}/{currency}")
def crypto_buing(account_id: str, currency: str):
    if currency != utils.EUR:
        raise HTTPException(status_code=404, detail="we support only EUR")
    if db.account_info(account_id):
        result = invest.buying(account_id, currency)

        return Response(content=json.dumps(result, default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")