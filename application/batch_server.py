import time
import schedule
import common.db as db
import common.utils as utils
import common.batch as batch


if utils.is_dev_env():
    batch.coinbase_job()
    batch.coinapi_job()
else:
    db.connection_param["host"] = "postgresql"
    if __name__ == '__main__':
        schedule.every(10).minutes.do(batch.tick_job)
        #schedule.every().hour.do(tick_job)
        schedule.every().day.at("14:30").do(batch.coinbase_job)
        schedule.every().day.at("13:30").do(batch.coinapi_job)

        #schedule.every(10).seconds.do(tick_job)
        #schedule.every(10).minutes.do(tick_job)
        #schedule.every(5).to(10).minutes.do(tick_job)
        #schedule.every().monday.do(tick_job)
        #schedule.every().wednesday.at("13:15").do(tick_job)
        #schedule.every().minute.at(":17").do(tick_job)

        while True:
            schedule.run_pending()
            time.sleep(1)