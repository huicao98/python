import time
import logging
import logging.config
from dp_spider.proxy_pool import ProxyPool
from dp_spider.runner import SpiderRunner
from dp_spider.spider import ShopSpider
from dp_spider.config import CONFIG, LOGGIN_CONFIG
from dp_spider.watcher import SpiderWather
from dp_spider import signals
from dp_spider.mapper import ShopMapper

s = time.ctime()
proxy_pool = None
success = []
if CONFIG.get('proxy', {}).get('enabled'):
    proxy_pool = ProxyPool(CONFIG.get('proxy', {}))
logging.config.dictConfig(LOGGIN_CONFIG)

runner = SpiderRunner(proxy_pool=proxy_pool)
spider_watcher = SpiderWather()

def scrap():
    # urls = ['https://www.dianping.com/search/keyword/1/0_%E7%BE%8E%E5%8F%91']
    # urls = ['https://m.dianping.com/shopshare/jZ9nV8sioSc8WAB1?msource=Appshare2021&utm_source=shop_share']
    # urls = ['https://www.dianping.com/shop/HafHYTwRfjlk6O0C',
    #         'https://www.dianping.com/shop/jZ9nV8sioSc8WAB1',
    #         'https://www.dianping.com/shop/k5T9BA4Xwa8NZkgU',
    #         'https://www.dianping.com/shop/l7Vmx6aOtc26PKdF']
    shops = ShopMapper.find_all_unsuccess_shops()
    if not shops:
        logging.warning('no shop available!')
        return
    
    spiders = []

    runner.run()
    for i, shop in enumerate(shops):
        try:
            # url = 'https://www.dianping.com/search/keyword/1/0_%E7%BE%8E%E5%8F%91'
            shop_spider = ShopSpider(
                id=shop.id,
                shop=shop,
                name=f'spider-{len(shops)}-{i+1}')
            spiders.append(shop_spider)
            spider_watcher.watch(signals.spider_response_processed_singal,
                                 shop_spider,
                                 spider_watcher.spider_response_processed)
            runner._enqueue_spider(shop_spider)
        except Exception as ex:
            logging.info(ex)
    spider_watcher.wait_until_all_processed()

    for spider in spiders:
        logging.info(f'success:{spider.success}--data: {spider.data}')
        spider_watcher.unwatch(signals.spider_response_processed_singal,
                               spider, spider_watcher.spider_response_processed)
    logging.info('run stop')
    runner.stop()

if __name__ == '__main__':
    scrap()
