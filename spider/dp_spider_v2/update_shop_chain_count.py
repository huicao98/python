# 更新连锁量
import time
import random
import logging
import logging.config as logging_config
from config import CONFIG,LOGGIN_CONFIG
from mapper import ShopMapper
logging_config.dictConfig(LOGGIN_CONFIG)

def run_update_shop_chain_count_sql():
    shops = ShopMapper.find_all_shops()
    page_size = 200
    page_num = len(shops) / 200.0
    print(f"total: {len(shops)} page_size: {page_size} page_num: {page_num}")

    current_page = 0
    while current_page<page_num:
        batch_shops = shops[current_page*page_size:(current_page+1)*page_size]
        print(f"total: {len(shops)} current_total:{len(batch_shops)}  page_size: {page_size} page_num: {page_num} current_page: {current_page}")
        ShopMapper.batch_update_chain_count(batch_shops)
        current_page+=1


    # for i,shop in enumerate(shops):
    #     print(f"total: {len(shops)} no: {i+1} shop: {shop}")
    #     ShopMapper.update_chain_count(shop=shop)

if __name__ == '__main__':
   run_update_shop_chain_count_sql()