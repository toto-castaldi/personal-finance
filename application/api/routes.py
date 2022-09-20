from re import U
import common.utils as utils
import common.db as db
import common.portfolio as portfolio
import common.portfolio_serialize as portfolio_serialize
import common.constants as constants
import common.bean as bean
import json
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

@app.get("/crypto-buying/{account_id}/{currency}")
def crypto_buing(account_id: str, currency: str):
    if currency != utils.EUR:
        raise HTTPException(status_code=404, detail="we support only EUR")
    if db.account_info(account_id):
        result = {}
        coinbase_movements = db.load_coinbase_crypto_trxs_by_user(account_id)
        moonpay_movements = db.load_moonpay_crypto_trxs_by_user(account_id)
        result["movements"] = [];
        result["total_amount"] = 0;
        result["total_currency"] = currency;
        for movement in coinbase_movements:
            if movement.type == utils.BUYING:
                if movement.native_amount_currency != currency:
                    if movement.native_amount_currency == utils.USD:
                        movement.native_amount_amount = utils.usd_to_eur(movement.native_amount_amount)
                    else:
                        ValueError(f"{movement.native_amount_currency} is an UNKNOW CURRENCY")
                m = bean.CryptoTransaction(
                    movement.id,
                    movement.native_amount_amount,
                    movement.updated_at, 
                    movement.crypto_amount_amount,
                    utils.PROVIDER_COINBASE,
                    movement.crypto_amount_currency,
                    movement.native_amount_currency

                )
                result["movements"].append(m)
                result["total_amount"] += m.native_amount_amount
        for movement in moonpay_movements:
            if movement.type == utils.BUYING and movement.status == utils.COMPLETED:
                if movement.native_amount_currency != currency:
                    if movement.native_amount_currency == utils.USD:
                        movement.native_amount_amount = utils.usd_to_eur(movement.native_amount_amount)
                        movement.fee_amount = utils.usd_to_eur(movement.fee_amount)
                        movement.extrafee_amount = utils.usd_to_eur(movement.extrafee_amount)
                        movement.networkfee_amount = utils.usd_to_eur(movement.fee_amount)
                        movement.native_amount_currency = utils.EUR
                    else:
                        ValueError(f"{movement.native_amount_currency} is an UNKNOW CURRENCY")
                m = bean.CryptoTransaction(
                    movement.id,
                    movement.native_amount_amount + movement.fee_amount + movement.extrafee_amount + movement.networkfee_amount,
                    movement.updated_at, 
                    movement.crypto_amount_amount,
                    utils.PROVIDER_MOONPAY,
                    movement.crypto_amount_currency,
                    movement.native_amount_currency
                )
                
                result["movements"].append(m)
                result["total_amount"] += m.native_amount_amount
        
        def sort_updated_at(e):
            return e.updated_at

        result["movements"].sort(key=sort_updated_at)

        return Response(content=json.dumps(result, default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")