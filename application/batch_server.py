import time
import schedule
import common.db as db
import common.utils as utils
import common.batch as batch


if utils.is_dev_env():
    batch.demo_data_job()
    #batch.coinbase_job()
    #batch.coinapi_job()
    pass
else:
    if __name__ == '__main__':
        schedule.every(10).minutes.do(batch.tick_job)

        #schedule.every().day.at("00:01").do(batch.coinapi_job)
        #schedule.every(2).hours.do(batch.coinbase_job)
        #schedule.every().day.at("01:00").do(batch.demo_data_job)

        schedule.every().day.at("10:17").do(batch.demo_data_job)
        schedule.every().day.at("10:18").do(batch.coinapi_job)
        
        #schedule.every().hour.do(tick_job)
        #schedule.every(10).seconds.do(tick_job)
        #schedule.every(10).minutes.do(tick_job)
        #schedule.every(5).to(10).minutes.do(tick_job)
        #schedule.every().monday.do(tick_job)
        #schedule.every().wednesday.at("13:15").do(tick_job)
        #schedule.every().minute.at(":17").do(tick_job)

        while True:
            schedule.run_pending()
            time.sleep(1)