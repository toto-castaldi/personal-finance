from datetime import date, datetime
from decimal import Decimal
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

SELECT_CRYPTO_FROM_TO = '''
select distinct(crypto_amount_currency, native_amount_currency) from coinbase_trx union all select distinct(name, 'EUR') from ethereum_rc20 er
'''

SELECT_CRYPTO_MIN_MAX_UPDATED_AT='''
select min(updated_at), max(updated_at) from (select updated_at from coinbase_trx ct union all select updated_at from public_ethereum_balance where smart_contract_address is null) aa;
'''

SELECT_COINBASE_TRX_MIN_MAX_UPDATED_AT_BY_ACCOUNT='''
select min(updated_at), max(updated_at) from coinbase_trx where account_id = %(account)s
'''

SELECT_BANK_MIN_MAX_UPDATED_AT_BY_ACCOUNT='''
select min(updated_at), max(updated_at) from bank_account_balance where account_id = %(account)s
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

SELECT_COINBASE_TRX_BY_ACCOUNT='''
select * from coinbase_trx where account_id = %(account)s 
'''

SELECT_MOONPAY_TRX_BY_ACCOUNT='''
select * from moonpay_trx where account_id = %(account)s 
'''

SELECT_PUBLIC_ADDRESSES_BY_ACCOUNT='''
select * from bitcoin_address where account_id = %(account)s
'''

SELECT_FINTABLES_BY_ACCOUNT='''
select * from fintable_user_base where account_id = %(account_id)s
'''

SELECT_PUBLIC_ETHEREUM_ADDRESSES_BY_ACCOUNT='''
select * from ethereum_address where account_id = %(account)s
'''

SELECT_DEGIRO_DEPOSIT_BY_ACCOUNT='''
select * from degiro_deposit where account_id = %(account_id)s
'''

SELECT_BANK_NAMES_BY_ACCOUNT='''
select distinct(bank_name) from bank_account_balance bab where account_id = %(account_id)s
'''

SELECT_SATISPAY_AT='''
select (risparmi_amount + disponibilita_amount) as amount from satispay where updated_at < %(updated_at)s and account_id = %(account_id)s order by updated_at desc limit 1
'''

SELECT_DEGIRO_AT='''
select * from degiro_account_balance where updated_at < %(updated_at)s and account_id = %(account_id)s order by updated_at desc limit 1
'''

SELECT_PUBLIC_BITCOIN_AT='''
select pbb.* from public_bitcoin_balance pbb, bitcoin_address ba  where pbb.public_address = ba.public_address and pbb.public_address = %(public_address)s and pbb.updated_at < %(updated_at)s and ba.account_id = %(account_id)s order by updated_at desc limit 1
'''

SELECT_BANK_AMOUNT_AT='''
select bab.* from bank_account_balance bab  where bab.bank_name = %(bank_name)s and bab.updated_at < %(updated_at)s and bab.account_id = %(account_id)s order by updated_at desc limit 1
'''

SELECT_PUBLIC_ETHEREUM_AT='''
select peb.* from (select * from public_ethereum_balance left join ethereum_rc20 on smart_contract_address = contract_address) peb, ethereum_address ea   where peb.public_address = ea.public_address and peb.updated_at < %(updated_at)s and ea.account_id = %(account_id)s and peb.smart_contract_address  is null order by updated_at desc limit 1
'''

SELECT_PUBLIC_ETHEREUM_RC20_AT='''
select peb.* from (select * from public_ethereum_balance left join ethereum_rc20 on smart_contract_address = contract_address) peb, ethereum_address ea   where peb.public_address = ea.public_address and peb.updated_at < %(updated_at)s and ea.account_id = %(account_id)s and peb.smart_contract_address = %(smart_contract_address)s order by updated_at desc limit 1
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

INSERT_SATISPAY = '''
INSERT INTO satispay (account_id, updated_at, risparmi_amount, disponibilita_amount, currency, image_name)
VALUES (%(account_id)s, %(updated_at)s, %(risparmi_amount)s, %(disponibilita_amount)s, %(currency)s, %(image_name)s)
'''

INSERT_MOONPAY_TRANSACTION = '''
INSERT INTO moonpay_trx
(account_id, trx_id, operation, native_amount_currency, native_amount_amount, updated_at, crypto_amount_amount, crypto_amount_currency, fee_amount, extrafee_amount, networkfee_amount, status)
VALUES(
  %(account_id)s, %(trx_id)s, %(operation)s, %(native_amount_currency)s, %(native_amount_amount)s, %(updated_at)s, %(crypto_amount_amount)s, 
  %(crypto_amount_currency)s, %(fee_amount)s, %(extrafee_amount)s, %(networkfee_amount)s, %(status)s)
on conflict (trx_id) do nothing;
'''

INSERT_DEGIRO_DEPOSIT = '''
INSERT INTO degiro_deposit
(account_id, updated_at, amount, currency)
VALUES(
  %(account_id)s, %(updated_at)s, %(amount)s, %(currency)s);
'''

INSERT_PUBLIC_ETHEREUM_ADDRESS = '''
INSERT INTO public_ethereum_balance (public_address, updated_at, amount, smart_contract_address)
VALUES (%(public_address)s, %(updated_at)s, %(amount)s, %(smart_contract_address)s)
'''

INSERT_BANK_ACCUNT_BALANCE = '''
INSERT INTO bank_account_balance (bank_name, updated_at, amount, currency, account_id)
VALUES (%(bank_name)s, %(updated_at)s, %(amount)s, %(currency)s, %(account_id)s)
'''

INSERT_DEGIRO_BALANCE = '''
INSERT INTO degiro_account_balance (updated_at, amount, currency, account_id, image_name)
VALUES (%(updated_at)s, %(amount)s, %(currency)s, %(account_id)s, %(image_name)s)
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

def load_bitcoin_addresses(account_id):
  return list(map(lambda e: e["public_address"],
    fetch(SELECT_PUBLIC_ADDRESSES_BY_ACCOUNT, {
      "account" : account_id
    }, all=True))
  )

def load_account_fintables(account):
  return list(map(lambda e: 
      bean.FintableAccount(
                            e["base_name"], 
                            e["api_key"]
      ),
    fetch(SELECT_FINTABLES_BY_ACCOUNT, {
      "account_id" : account.id
    }, all=True))
  )
  

def load_ethereum_addresses(account):
  return list(map(lambda e: e["public_address"],
    fetch(SELECT_PUBLIC_ETHEREUM_ADDRESSES_BY_ACCOUNT, {
      "account" : account.id
    }, all=True))
  )

def load_degiro_deposits_by_user(account_id):
  return list(map(lambda e: 
      bean.DegiroDeposit(
                            e["updated_at"], 
                            e["amount"],  
                            e["currency"]
      ),
    fetch(SELECT_DEGIRO_DEPOSIT_BY_ACCOUNT, {
      "account_id" : account_id
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

def load_coinbase_crypto_trxs_by_user(account:str):
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
    fetch(SELECT_COINBASE_TRX_BY_ACCOUNT, {
      "account" : account
    }, all=True))
  )

def load_moonpay_crypto_trxs_by_user(account:str):
  return list(map(lambda e: 
      bean.MoonpayTransaction(
                            e["trx_id"], 
                            e["operation"], 
                            Decimal(e["native_amount_amount"]),  
                            e["native_amount_currency"],
                            e["updated_at"], 
                            e["crypto_amount_amount"],  
                            e["crypto_amount_currency"],
                            e["fee_amount"],
                            e["extrafee_amount"],
                            e["networkfee_amount"],
                            e["status"]
      ),
    fetch(SELECT_MOONPAY_TRX_BY_ACCOUNT, {
      "account" : account
    }, all=True))
  )

def min_max_coinbase_date_trx_by_account(account):
  min_max = fetch(SELECT_COINBASE_TRX_MIN_MAX_UPDATED_AT_BY_ACCOUNT, {
    "account" : account
  })
  return min_max["min"], min_max["max"]

def min_max_bank_by_account(account):
  min_max = fetch(SELECT_BANK_MIN_MAX_UPDATED_AT_BY_ACCOUNT, {
    "account" : account
  })
  return min_max["min"], min_max["max"]

def min_max_public_bitcoins_date_trx_by_account(account):
  min_max = fetch(SELECT_PUBLIC_BITCOIN_MIN_MAX_UPDATED_AT_BY_ACCOUNT, {
    "account" : account
  })
  return min_max["min"], min_max["max"]

def crypto_from_to():
  return list(map(lambda e: tuple(e["row"][1:-1].split(',')), fetch(SELECT_CRYPTO_FROM_TO, all=True)))

def min_max_date_trx():
  min_max = fetch(SELECT_CRYPTO_MIN_MAX_UPDATED_AT)
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

def load_public_bitcoins_amount_at(the_date: date, account_id: str, public_address: str):
  c = fetch(SELECT_PUBLIC_BITCOIN_AT, {
    "updated_at" : the_date,
    "account_id" : account_id,
    "public_address" : public_address
  })
  if c :
    return c["amount"]
  else:
    return None

def load_satispay_balances_at(the_date, account_id):
  c = fetch(SELECT_SATISPAY_AT, {
    "updated_at" : the_date,
    "account_id" : account_id
  })
  if c :
    return c["amount"]
  else:
    return None

def load_degiro_balances_at(the_date, account_id):
  c = fetch(SELECT_DEGIRO_AT, {
    "updated_at" : the_date,
    "account_id" : account_id
  })
  if c :
    return c["amount"]
  else:
    return None

def load_bank_accout_balances_at(the_date, account_id):
  bank_names = list(map(lambda e: e["bank_name"],
    fetch(SELECT_BANK_NAMES_BY_ACCOUNT, {
      "account_id" : account_id
    }, all=True))
  )
  result = []
  for bank_name in bank_names:
    c = fetch(SELECT_BANK_AMOUNT_AT, {
      "updated_at" : the_date,
      "account_id" : account_id,
      "bank_name" : bank_name
    })
    if c :
      result.append((bank_name, c["amount"]))

  return result;
    
def load_public_ethers_amount_at(the_date, account, smart_contract_address):
  c = fetch(SELECT_PUBLIC_ETHEREUM_AT if smart_contract_address is None else SELECT_PUBLIC_ETHEREUM_RC20_AT, {
    "updated_at" : the_date,
    "account_id" : account,
    "smart_contract_address" : smart_contract_address
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

def save_satispay(account_id : str, today : date, disponibilita_euro : Decimal, risparmi_euro: Decimal, currency: str, image_name: str):
  with get_conn() as conn:  
      with conn.cursor() as cursor:
        cursor.execute(INSERT_SATISPAY, {
          "account_id" : account_id,
          "updated_at" : today,
          "risparmi_amount" : risparmi_euro,
          "disponibilita_amount" : disponibilita_euro,
          "currency" : currency,
          "image_name" : image_name
        })

def save_moonpay_transaction(account_id : str, today : date, row):
  # account_id, trx_id, operation, native_amount_currency, native_amount_amount, updated_at, crypto_amount_amount, crypto_amount_currency, fee_amount, extrafee_amount, networkfee_amount, status
  # ['1311654b-b5f0-4351-a973-9d08998a9df2', 'buy', 'usd', '478.86', '2022-03-10T10:14:19.447Z', 'eth', '', '15.56', '4.55', '1.03', 'failed']

  with get_conn() as conn:  
      with conn.cursor() as cursor:
        cursor.execute(INSERT_MOONPAY_TRANSACTION, {
          "account_id" : account_id,
          "trx_id" : row[0],
          "operation" : row[1],
          "native_amount_currency" : utils.native_currency(row[2]),
          "native_amount_amount" :row[3],
          "updated_at" :row[4],
          "crypto_amount_currency" :utils.crypto_currency(row[5]),
          "crypto_amount_amount" : row[6] if len(row[6]) > 0 else 0, 
          "fee_amount" : row[7],
          "extrafee_amount" : row[8],
          "networkfee_amount" : row[9],
          "status" : row[10],
        })

def save_degiro_deposit(account_id : str, today : date, row):
  # ['28-09-2022', '10:50', '28-09-2022', '', '', 'Deposito flatex', '', 'EUR', '400,00', 'EUR', '420,43', '']
  logger.debug(row)
  logger.debug(account_id)
  with get_conn() as conn:  
      with conn.cursor() as cursor:
        cursor.execute(INSERT_DEGIRO_DEPOSIT, {
          "account_id" : account_id,
          "updated_at" : datetime.strptime(row[0], '%d-%m-%Y'),
          "amount" : utils.str_euro_to_number(row[8]),
          "currency" : row[7]
        })

def save_degiro_transaction(account_id : str, today : date, row):
  pass

def save_address_ethereum_amount(today, address, bitcoin_amount, smart_contract):
  with get_conn() as conn:  
      with conn.cursor() as cursor:
        cursor.execute(INSERT_PUBLIC_ETHEREUM_ADDRESS, {
          "updated_at" : today,
          "public_address" : address,
          "amount" : bitcoin_amount,
          "smart_contract_address" : smart_contract
        })

def save_bank_account_balance(account_id : str, today : date, name : str, balance : Decimal, currency : str):
  with get_conn() as conn:  
      with conn.cursor() as cursor:
        cursor.execute(INSERT_BANK_ACCUNT_BALANCE, {
          "account_id" : account_id,
          "updated_at" : today,
          "amount" : balance,
          "bank_name" : name,
          "currency" : currency
        })

def save_degiro_balance(account_id : str, today : date, balance : Decimal, currency : str, image_name : str = None):
  with get_conn() as conn:  
      with conn.cursor() as cursor:
        cursor.execute(INSERT_DEGIRO_BALANCE, {
          "account_id" : account_id,
          "updated_at" : today,
          "amount" : balance,
          "currency" : currency,
          "image_name" : image_name
        })