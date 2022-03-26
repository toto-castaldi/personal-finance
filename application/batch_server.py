import time
import schedule
import common.utils as utils
import common.user_demo as user_demo
import common.companion_image as companion_image
import common.companion_csv as companion_csv
import common.fiintable as fintable
import common.coinapi as coinapi
import common.coinbase as coinbase
import common.blockchaincom as blockchaincom
import common.etherscan as etherscan


logger = utils.init_log()

def tick_job():
    logger.info("tick...")


if utils.is_dev_env():
    companion_image.job()
    pass
else:
    if __name__ == '__main__':
        companion_image.job()
        companion_csv.job()

        schedule.every(10).minutes.do(tick_job)
        
        schedule.every().day.at("00:01").do(user_demo.demo_data_job)

        schedule.every().day.at("00:10").do(coinapi.coinapi_job)
        schedule.every().day.at("00:20").do(coinbase.coinbase_job)
        schedule.every().day.at("00:30").do(blockchaincom.blockchaincom_job)
        schedule.every().day.at("00:40").do(etherscan.etherscan_job)
        schedule.every().day.at("00:50").do(fintable.fintable_job)
        schedule.every().day.at("01:00").do(companion_image.job)
        schedule.every().day.at("01:10").do(companion_csv.job)

        #schedule.every(10).minutes.do(batch.companion_images_job)
        
        #schedule.every().day.at("01:00").do(batch.demo_data_job)
        #schedule.every().day.at("10:17").do(batch.demo_data_job)
        #schedule.every().day.at("10:18").do(batch.coinapi_job)
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