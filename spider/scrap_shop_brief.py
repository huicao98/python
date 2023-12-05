from dp_spider.mapper import ShopMapper
import time
import logging
import logging.config
import os
import sys
from pyquery import PyQuery as pq
from dp_spider.mapper import ShopMapper,Shop


from dp_spider.config import CONFIG, LOGGIN_CONFIG
logging.config.dictConfig(LOGGIN_CONFIG)


def run():
    # TODO ch 按需填写
    # data_path = f'{os.getcwd()}/data/001-sh'
    data_path =  '/home/charlot/data/spider/sh'
    logging.info(f'data path: {data_path}')
    for i in sorted(os.listdir(data_path)):
        file_path = f'{data_path}/{i}'
        if os.path.isdir(file_path):
            continue
        logging.info(f'process {i}')
        doc = pq(filename=file_path)
        shop_elements = doc("a[data-hippo-type='shop']")
        shops = []
        # TODO ch 解析团购
        for shop_element in shop_elements:
            shop = Shop()
            for k,v in dict(shop_element.items()).items():
                if k=='data-shopid':
                    shop.code = v
                if k=='title':
                    shop.name = v
            shop.data_source = i
            shops.append(shop)
        if shops:
            ShopMapper.create_shops(shops)


if __name__ == '__main__':
    run()
