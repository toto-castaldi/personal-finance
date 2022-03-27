from re import U
import common.utils as utils
import common.db as db
import common.portfolio as portfolio
import common.portfolio_serialize as portfolio_serialize
import common.constants as constants
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
    with open(filename, "wb") as f:
        f.write(contents)

    return {"result": "ok"}

@app.get("/portfolio-values/{account_id}/{currency}/{max_num_of_points}")
def portfolio_values_json(account_id: str, currency: str, max_num_of_points : int):
    logger.debug(account_id)
    if db.account_info(account_id):
        return Response(content=json.dumps(
            portfolio_serialize.asset_points(
                portfolio.Portfolio(account_id), 
                currency,
                max_num_of_points
            ), 
            default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/portfolio-summary/{account_id}/{currency}")
def portfolio_values_json(account_id: str, currency: str):
    if db.account_info(account_id):
        return Response(content=json.dumps(portfolio_serialize.summary(portfolio.Portfolio(account_id), native_currency=currency), default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")

@app.get("/portfolio-level/{account_id}/{level}/{node}")
def portfolio_level(account_id: str, level: int, node : str):
    if db.account_info(account_id):
        nodes = portfolio_serialize.level(portfolio.Portfolio(account_id), level, node);
        return Response(content=json.dumps(nodes, default=utils.json_serial), media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="wrong account")