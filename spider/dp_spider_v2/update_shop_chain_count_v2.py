# 更新连锁量
import time
import random
import logging
import logging.config as logging_config
from config import CONFIG,LOGGIN_CONFIG
from mapper import ShopMapper
logging_config.dictConfig(LOGGIN_CONFIG)

def run_update_shop_chain_count_sql():
    logging.info(">>> 开始运行，请耐心等待....")
    ShopMapper.batch_update_chain_count2()
    logging.info(">>> 运行成功!")
    
if __name__ == '__main__':
   run_update_shop_chain_count_sql()