# 获取点评评论
import argparse
import os
import time
import random
import logging
import plyer
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
from pyquery import PyQuery as pq
import re
import json
from config import CONFIG,LOGGIN_CONFIG
from browser import BrowserFactory
from mapper import ShopMapper
from get_dp_cookie import get_cookie
from plyer import notification
from utils import sanitize_text,sanitize_cost
from wifi import switch_wifi,release_switch_wifi_lock
logging.config.dictConfig(LOGGIN_CONFIG)

from dotenv import find_dotenv, load_dotenv,get_key, set_key
load_dotenv(find_dotenv('env'))

class SpiderBlockedException(Exception):
    def __init__(self,message=None):
        super().__init__(message or '被封锁了，请处理')


class SpiderBlockedNeedSwitchWIFIException(SpiderBlockedException):
    def __init__(self,message=None):
        super().__init__(message or 'WIFI被封锁了，请处理')

class SpiderDownloadPageException(Exception):
    def __init__(self,message=None):
        super().__init__(message or '进入下载页面了')
        
class SpiderVerifyException(Exception):
    def __init__(self,message=None):
        super().__init__(message or '身份核实，请处理')

def get_dp_basic(城市=[],行政区=[],地区=[]):
    driver = BrowserFactory.create_browser(config=CONFIG)
    # 行政区= [] 代表全部
    # 地区=[] 代表全部
    while True:
        shops = []
        try:
            shops = ShopMapper.find_all_unscrape_basic_shops(城市=城市,行政区=行政区,地区 = 地区 )
        except Exception as e:
            logging.error(str(e))
            print(f"查询店铺错误：{e}")
            time.sleep(2)
            continue

        if len(shops)==0:
            logging.info('******任务执行完成啦************')
            break
        try:
             for i,shop in enumerate(shops):
                try:
                    print(f"total: {len(shops)} no: {i+1} left: {len(shops)-i-1} shop: {shop}")
                    _run_get_dp_basic_from_m_share(shop=shop,driver=driver)
                except SpiderDownloadPageException as e1:
                    logging.error(f"进入了下载页面错误>> {shop}")
                    _run_get_dp_basic_from_m_share(shop=shop,driver=driver)
        except SpiderBlockedNeedSwitchWIFIException as e1:
             notification.notify(title="账号被封", message='WIFI被封锁了，请处理', timeout=5)
             logging.error('WIFI被封锁了，请处理')
             try:
                switch_wifi()
                # pass
             except Exception as e:
                print(e)
                continue
        except SpiderBlockedException as e:
            if 'verify.meituan.com' in driver.current_url:
                notification.notify(title="身份核验", message="点评身份核验", timeout=5)
            else:
                notification.notify(title="账号被封", message="账号掉线或者需要验证", timeout=5)
            while True:
                 print("""!!!!!!!!!!!!!!!
                            !!!!!!! token expired !!!!!!!
                                !!!!!!!!!!!!!""")
                 time.sleep(1)
                 if 'verify.meituan.com' in driver.current_url:
                     continue
                 break
        except SpiderVerifyException as e1:
            notification.notify(title="身份核验", message="点评身份核验", timeout=5)
        finally:
            pass

def _run_get_dp_basic_from_m_share(shop,driver):
    try:
        mobile_share_url = f'https://m.dianping.com/shopshare/{shop.code}?msource=Appshare2021&utm_source=shop_share'
        logging.info('mobile url>>>> '+mobile_share_url)
        driver.get(mobile_share_url)
        try:
            # case 1
            WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'shopname'))
            )
        except WebDriverException:
            if driver.current_url == 'https://h5.dianping.com/app/app-m-user-growth/download.html':
                raise SpiderDownloadPageException()

            try:
                # case 2
                WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'shopName'))
                )
            except WebDriverException:
                 if driver.current_url == 'https://h5.dianping.com/app/app-m-user-growth/download.html':
                    raise SpiderDownloadPageException()
        mobile_page_source = driver.page_source
        mobile_doc = pq(mobile_page_source)
                
        # case 1 https://m.dianping.com/shopshare/GamLG6UWRFE4a5k2?msource=Appshare2021&utm_source=shop_share
        mobile_addresses1 = mobile_doc(".i-add")
        if mobile_addresses1:
            try:
                mobile_address1 = sanitize_text(mobile_addresses1[0].tail)
                shop.点评地址 = mobile_address1
            except:
                pass

        score = mobile_doc(".scoreText")
        if score:
            scoreText = sanitize_text(score.text())
            shop.点评评分 = scoreText
        
        
        reviews = mobile_doc(".reviews")
        if reviews:
            try:
                reviews = sanitize_text(reviews[0].text)
                shop.评价 = reviews
            except:
                pass

        # case 2 https://m.dianping.com/shopshare/l8sHSfJlKfT4zq7g?msource=Appshare2021&utm_source=shop_share
        if not shop.点评地址:
            mobile_addresses2 = mobile_doc(".addressText")
            if mobile_addresses2:
                mobile_address2 = sanitize_text(mobile_addresses2[0].text)
                shop.点评地址 = mobile_address2

        
        # case 1 https://m.dianping.com/shopshare/GamLG6UWRFE4a5k2?msource=Appshare2021&utm_source=shop_share
        costs1 = mobile_doc(".aver")
        if  shop.人均价格 is None or  shop.人均价格=='':
            if costs1:
                try:
                    cost1 = sanitize_cost(costs1[0].text)
                    shop.人均价格 = cost1
                except:
                    pass
                        
        # case 2: https://m.dianping.com/shopshare/H7iFIVUmEDXo1DhS?msource=Appshare2021&utm_source=shop_share
        if  shop.人均价格 is None or  shop.人均价格=='':
            costs2 = mobile_doc(".price")
            if costs2:
                try:
                    shop.人均价格 = sanitize_cost(costs2[0].text)
                except:
                    pass

        # case 1 https://m.dianping.com/shopshare/GamLG6UWRFE4a5k2?msource=Appshare2021&utm_source=shop_share
        if not shop.点评电话:
            mobile_tels = mobile_doc("#telphone")
            if mobile_tels:
                for k,v in dict(mobile_tels[0].items()).items():
                    if k=='href':
                        mobile_tel = sanitize_text( v.replace('tel:',''))
                        shop.点评电话 = mobile_tel

        # case 2 https://m.dianping.com/shopshare/H7iFIVUmEDXo1DhS?msource=Appshare2021&utm_source=shop_share
        if not shop.点评电话:
            json_cache= json.loads(mobile_doc('body>script')[0].text.replace('window.__xhrCache__ = ',''))
            for k,v in json_cache.items():
                if 'data' in v and 'phoneNos' in v['data']:
                    tels2 = v['data']['phoneNos']
                    if tels2:
                        mobile_tel2 = ','.join(tels2)
                        shop.点评电话 = mobile_tel2
        # 店铺状态
        stop_status = mobile_doc(".shopStatus")
        if stop_status:
            shopStatus = sanitize_text(stop_status.text())
            shop.店铺状态 = shopStatus
        else:
            shop.店铺状态 = '正常营业'
        
        print(f">>>>> get shop : {shop}")
        ShopMapper.update_shop_basic(shop=shop)
    except SpiderDownloadPageException as e:
        raise e
    except Exception as e4:
        # 访问的店铺不存在 https://m.dianping.com/shopshare/G7n53cVDhR8vqk7W?msource=Appshare2021&utm_source=shop_share
        if driver.current_url == 'https://h5.dianping.com/app/app-m-user-growth/download.html':
            raise SpiderDownloadPageException()
        if 'verify.meituan.com' in driver.current_url:
          raise  SpiderBlockedException()
        
        try:
            h1 = driver.find_element(By.TAG_NAME,'h1')
            if h1.text=='403 Forbidden':
                # 重新换token
                logging.error('token expired')

                print("""!!!!!!!!!!!!!!!
                        !!!!!!! token expired !!!!!!!
                            !!!!!!!!!!!!!""")
                raise SpiderBlockedNeedSwitchWIFIException()
        except SpiderBlockedNeedSwitchWIFIException  as e6:
                raise e6
        except NoSuchElementException:
                pass
        
        is_ok_logic = False
        try:
            prev = driver.find_element(By.TAG_NAME,'pre')
            if  '您访问的页面不存在' in prev.text:
                shop.店铺状态 = '商户暂停收录'
                ShopMapper.update_shop_basic(shop=shop)
                is_ok_logic = True
        except WebDriverException as e5:
            pass

        if not is_ok_logic:
            logging.error(e4, exc_info=True, stack_info=True)
            raise SpiderBlockedException()

                    
    # time.sleep(random.randint(1,3))
    return True




parser = argparse.ArgumentParser(description='参数')
parser.add_argument('--城市', 
                    dest='城市',
                    default='',
                    help='城市')

parser.add_argument('--行政区', 
                    dest='行政区',
                    default='',
                    help='行政区')

parser.add_argument('--地区', 
                    dest='地区',
                    default='',
                    help='地区')

if __name__ == '__main__':
    """
        使用示例： 
        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=淄博市 --行政区=张店区,淄川,临淄,沂源县
        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=淄博市 --行政区=恒台县,周村,博山,高青县
        
        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=株洲市

        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=天津市 --行政区=滨海新区,南开区,津南区
        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=天津市 --行政区=和平区,河西区,武清区,西青区
        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=天津市 --行政区=河东区,北辰区,河北区,东丽区
        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=天津市 --行政区=静海区,蓟州区,红桥区,宝坻区,宁河区


        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=沈阳市 --行政区=沈河区
        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=沈阳市 --行政区=于洪区
        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=沈阳市 --行政区=浑南区
        python dp_spider_v2/scrap_dp_basic_from_h5.py --城市=沈阳市 --行政区=铁西区,沈北新区


   """
    城市=['上海市']
    行政区=[]
    地区=[]
    args = parser.parse_args()
    if args.城市:
        城市 = args.城市.split(',')
    if args.行政区:
        行政区 = args.行政区.split(',')
    if args.地区:
        地区 = args.地区.split(',')
    print('城市: ',城市,'行政区: ',行政区,'地区: ',地区)
    release_switch_wifi_lock()
    get_dp_basic(城市=城市,行政区=行政区,地区=地区)
    release_switch_wifi_lock()