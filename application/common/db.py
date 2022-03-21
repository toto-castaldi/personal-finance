import psycopg2
import common.utils as utils
import common.bean as bean
from psycopg2.extras import RealDictCursor
from dataclasses import asdict

connection_param = {
        "dbname" : "dbpsql", 
        "user" : "dbpsql", 
        "password" : "dbpsql", 
        "host" : "localhost",
        "port" : 5432
    }

conn = None

logger = utils.init_log()

if utils.is_dev_env() is not True:
  connection_param["host"] = "postgresql"

SELECT_ALL_ACCOUNTS = '''
SELECT * FROM ACCOUNT
'''

SELECT_ALL_RC20 = '''
SELECT * FROM ETHEREUM_RC20
'''

SELECT_ACCOUNT_INFO = '''
SELECT * FROM ACCOUNT where account_id = %(account_id)s
'''

SELECT_COINBASE_TRX_FROM_TO = '''
select distinct(crypto_amount_currency, native_amount_currency) from coinbase_trx 
'''

SELECT_COINBASE_TRX_MIN_MAX_UPDATED_AT='''
select min(updated_at), max(updated_at) from coinbase_trx ;
'''

SELECT_COINBASE_TRX_MIN_MAX_UPDATED_AT_BY_ACCOUNT='''
select min(updated_at), max(updated_at) from coinbase_trx where account_id = %(account)s
'''

SELECT_PUBLIC_BITCOIN_MIN_MAX_UPDATED_AT_BY_ACCOUNT='''
select min(pbb.updated_at), max(pbb.updated_at) from public_bitcoin_balance pbb, bitcoin_address ba  where pbb.public_address = ba.public_address and ba.account_id = %(account)s
'''

SELECT_CRYPTO_RATE='''
 select amount from crypto_rate where crypto_currency = %(crypto_currency)s and native_currency = %(native_currency)s and date = %(date)s;
'''

SELECT_COINBASE_TRX_BY_ACCOUN_DATES='''
select * from coinbase_trx where account_id = %(account)s and updated_at >= %(date_from)s and updated_at < %(date_to)s
'''

SELECT_PUBLIC_ADDRESSES_BY_ACCOUNT='''
select * from bitcoin_address where account_id = %(account)s
'''

SELECT_PUBLIC_ETHEREUM_ADDRESSES_BY_ACCOUNT='''
select * from ethereum_address where account_id = %(account)s
'''

SELECT_PUBLIC_BITCOIN_AT='''
select pbb.* from public_bitcoin_balance pbb, bitcoin_address ba  where pbb.public_address = ba.public_address and pbb.updated_at <= %(updated_at)s and ba.account_id = %(account_id)s order by updated_at desc limit 1
'''

INSERT_COINBASE_TRANSACTION = '''
INSERT INTO coinbase_trx (account_id, trx_id, updated_at, native_amount_amount, crypto_amount_amount, buy_sell, native_amount_currency, crypto_amount_currency)
VALUES (%(account_id)s, %(id)s, %(updated_at)s, %(native_amount_amount)s, %(crypto_amount_amount)s, %(type)s, %(native_amount_currency)s, %(crypto_amount_currency)s)
on conflict (trx_id) do nothing;
'''

INSERT_CRYPTO_RATE = '''
INSERT INTO crypto_rate (crypto_currency, native_currency, date, amount)
VALUES (%(crypto_currency)s, %(native_currency)s, %(date)s, %(amount)s)
on conflict (crypto_currency, native_currency, date) do nothing;
'''

INSERT_PUBLIC_BITCOIN_ADDRESS = '''
INSERT INTO public_bitcoin_balance (public_address, updated_at, amount)
VALUES (%(public_address)s, %(updated_at)s, %(amount)s)
'''

INSERT_PUBLIC_ETHEREUM_ADDRESS = '''
INSERT INTO public_ethereum_balance (public_address, updated_at, amount, smart_contract_address)
VALUES (%(public_address)s, %(updated_at)s, %(amount)s, %(smart_contract_address)s)
'''

def get_conn():
  global conn

  if conn:
    try: 
      with conn.cursor() as cursor:
        cursor.execute("SELECT 1")
    except:
      conn = None

  if not conn and connection_param:
    logger.debug(connection_param)
    conn = psycopg2.connect(dbname=connection_param["dbname"], user=connection_param["user"], password=connection_param["password"], host=connection_param["host"], port=connection_param["port"], cursor_factory=RealDictCursor)
       
  return conn


def fetch(query, args={}, all=False):
  with get_conn() as conn:   
    with conn.cursor() as cursor:
      cursor.execute(query, args)
      result = cursor.fetchall() if all else cursor.fetchone()
      return result

def account_info(account_id):
  c = fetch(SELECT_ACCOUNT_INFO, {
    "account_id" : account_id,
  })
  if c:
    return bean.Account(c["account_id"], c["coinbase_api_key"], c["coinbase_api_secret"])
  else:
    return None

def load_all_accounts():
  return list(map(lambda e: bean.Account(e["account_id"], e["coinbase_api_key"], e["coinbase_api_secret"]), fetch(SELECT_ALL_ACCOUNTS, all=True)))

def load_all_rc20():
  return list(map(lambda e: bean.RC20(e["name"], e["contract_address"]), fetch(SELECT_ALL_RC20, all=True)))

def load_bitcoin_addresses(account):
  return list(map(lambda e: e["public_address"],
    fetch(SELECT_PUBLIC_ADDRESSES_BY_ACCOUNT, {
      "account" : account.id
    }, all=True))
  )

def load_ethereum_addresses(account):
  return list(map(lambda e: e["public_address"],
    fetch(SELECT_PUBLIC_ETHEREUM_ADDRESSES_BY_ACCOUNT, {
      "account" : account.id
    }, all=True))
  )
    
def load_coinbase_crypto_trxs_by_user_and_date(account, down_range, up_range):
  return list(map(lambda e: 
      bean.CoinbaseTransaction(
                            e["trx_id"], 
                            e["updated_at"], 
                            e["native_amount_amount"],  
                            e["native_amount_currency"],
                            e["buy_sell"],
                            e["crypto_amount_amount"],  
                            e["crypto_amount_currency"]
      ),
    fetch(SELECT_COINBASE_TRX_BY_ACCOUN_DATES, {
      "account" : account,
      "date_from" : down_range,
      "date_to" : up_range
    }, all=True))
  )

def min_max_coinbase_date_trx_by_account(account):
  min_max = fetch(SELECT_COINBASE_TRX_MIN_MAX_UPDATED_AT_BY_ACCOUNT, {
    "account" : account
  })
  return min_max["min"], min_max["max"]

def min_max_public_bitcoins_date_trx_by_account(account):
  min_max = fetch(SELECT_PUBLIC_BITCOIN_MIN_MAX_UPDATED_AT_BY_ACCOUNT, {
    "account" : account
  })
  return min_max["min"], min_max["max"]

def coinbase_currency_from_to():
  return list(map(lambda e: tuple(e["row"][1:-1].split(',')), fetch(SELECT_COINBASE_TRX_FROM_TO, all=True)))

def min_max_date_trx():
  min_max = fetch(SELECT_COINBASE_TRX_MIN_MAX_UPDATED_AT)
  return min_max["min"], min_max["max"]

def get_crypto_rate(the_date, crypto_currency, native_currency):
  c = fetch(SELECT_CRYPTO_RATE, {
    "crypto_currency" : crypto_currency,
    "native_currency" : native_currency,
    "date" : the_date
  })
  if c :
    return c["amount"]
  else:
    return None

def load_public_bitcoins_amount_at(the_date, account):
  c = fetch(SELECT_PUBLIC_BITCOIN_AT, {
    "updated_at" : the_date,
    "account_id" : account
  })
  if c :
    return c["amount"]
  else:
    return None

def merge_transactions(user, transactions):
  logger.debug(user)
  for transaction in transactions:  
    with get_conn() as conn:  
      with conn.cursor() as cursor:
        arg = asdict(transaction)
        arg["account_id"] = user.id
        logger.debug(arg)
        cursor.execute(INSERT_COINBASE_TRANSACTION, arg)

def save_crypto_rate(the_date, currency_from, currency_to, rate):
  with get_conn() as conn:  
      with conn.cursor() as cursor:
        cursor.execute(INSERT_CRYPTO_RATE, {
          "crypto_currency" : currency_from,
          "native_currency" : currency_to,
          "date" : the_date,
          "amount" : rate
        })

def save_address_bitcoin_amount(today, address, bitcoin_amount):
  with get_conn() as conn:  
      with conn.cursor() as cursor:
        cursor.execute(INSERT_PUBLIC_BITCOIN_ADDRESS, {
          "updated_at" : today,
          "public_address" : address,
          "amount" : bitcoin_amount
        })

def save_address_ethereum_amount(today, address, bitcoin_amount, smart_contract):
  with get_conn() as conn:  
      with conn.cursor() as cursor:
        cursor.execute(INSERT_PUBLIC_ETHEREUM_ADDRESS, {
          "updated_at" : today,
          "public_address" : address,
          "amount" : bitcoin_amount,
          "smart_contract_address" : smart_contract
        })