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
from config import CONFIG,LOGGIN_CONFIG
from browser import BrowserFactory
from mapper import ShopMapper
from get_dp_cookie import get_cookie
from plyer import notification
logging.config.dictConfig(LOGGIN_CONFIG)

from dotenv import find_dotenv, load_dotenv,get_key, set_key
load_dotenv(find_dotenv('local_env'))

class SpiderBlockedException(Exception):
    def __init__(self,message=None):
        super().__init__(message or '被封锁了，请处理')

class SpiderVerifyException(Exception):
    def __init__(self,message=None):
        super().__init__(message or '身份核实，请处理')

def get_dp_comment(driver=None,城市=[],行政区=[],地区=[]):
    if not driver:
        driver = BrowserFactory.create_browser(config=CONFIG)
    print('driver--->', driver)
    driver.get('https://www.dianping.com/')
    driver = get_cookie(driver=driver)
    
    time.sleep(1)
    driver.add_cookie({
            'name': 'dper',
            'value': get_key('local_env','cookie_dper'),
        })
    # 行政区= [] 代表全部
    # 地区=[] 代表全部
    # 城市 = ['深圳市']
    # 行政区= ['福田区','南山区','罗湖区','盐田区','大鹏新区','龙华区']
    # 行政区= ['龙岗区','宝安区','坪山区','光明区']
    # 地区= []
  
    while True:
        shops = ShopMapper.find_all_unscrape_basic_shops(城市=城市,行政区=行政区,地区 = 地区 )
        if len(shops)==0:
            logging.info('******任务执行完成啦************')
            break
        try:
            _run_get_dp_comment(shops=shops, driver=driver)
        except SpiderBlockedException as e:
            notification.notify(title="扫码登录", message="点评重新扫码登录", timeout=5)
            get_cookie(driver=driver)
        except SpiderVerifyException as e1:
            notification.notify(title="身份核验", message="点评身份核验", timeout=5)
        finally:
            pass

def _run_get_dp_comment(shops, driver):
    for i,shop in enumerate(shops):
        print(f"total: {len(shops)} no: {i+1} left: {len(shops)-i-1} shop: {shop}")
        url = shop.店铺_详情

        try:
            driver.get(url)
            shop.点评电话 = ''
            shop.点评地址 = ''
            shop.点评评分 = ''
            shop.人均价格 = ''
            shop.评价 = ''
            shop.店铺状态 = '正常营业'
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'shop-name'))
            )
            shopname = driver.find_element(By.CLASS_NAME,'shop-name')
            try:
                shop.点评电话 = driver.find_element(By.CSS_SELECTOR, 'p.expand-info.tel').text
            except:
                print("手机号获取失败")
            try:
                shop.点评地址 = driver.find_element(By.XPATH, '//*[@id="address"]').text
            except:
                print('地址获取失败')
            try:
                shop.点评评分 = driver.find_element(By.XPATH, '//*[@id="comment_score"]').text
            except:
                print('评分获取失败')
            try:
                shop.人均价格 = driver.find_element(By.ID, 'avgPriceTitle').text
            except:
                print('人均价格获取失败')
            try:
                shop.评价 = driver.find_element(By.ID, 'reviewCount').text
            except:
                print('评价获取失败')
            try:
                shop.店铺状态 = driver.find_element(By.CLASS_NAME, 'shop-closed').text
            except Exception as e:
                pass
            try:
                shop.店铺状态 = driver.find_element(By.CLASS_NAME, 'trumpet-text').text
            except Exception as e:
                pass
            
            ShopMapper.update_shop_basic(shop)

        except WebDriverException as e:
            logging.error(f"获取错误1: {e.msg}")
            # 404
            try:
                title = driver.find_element(By.TAG_NAME,'title')
                if '404 | 大众点评网' in title.text or '404 | 大众点评网' in driver.title:
                    shop.店铺状态 = '商户暂停收录'
                    ShopMapper.update_shop_basic(shop=shop)
                    continue
            except WebDriverException as e5:
                pass

            try:
                # 是否有滑块
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'dpLogo'))
                )
                logo = driver.find_element(By.CLASS_NAME, "dpLogo").text
                if logo == '身份核实':
                    raise SpiderVerifyException()
            except WebDriverException:
                pass

            try:
                h1 = driver.find_element(By.TAG_NAME,'h1')
                if h1.text=='403 Forbidden':
                    # 重新换token
                    logging.error('token expired')

                    print("""!!!!!!!!!!!!!!!
                        !!!!!!! token expired !!!!!!!
                            !!!!!!!!!!!!!""")
                    raise SpiderBlockedException()
            except SpiderBlockedException  as e6:
                raise e6
            except NoSuchElementException:
                pass
        except SpiderVerifyException as e5:
            raise e5
        except Exception as e4:
            raise SpiderBlockedException()

                        
        time.sleep(random.randint(1,3))
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
        
        python dp_spider_v2/scrap_dp_basic_from_pc.py --城市=郑州市 --行政区=金水区,二七区
        python dp_spider_v2/scrap_dp_basic_from_pc.py --城市=郑州市 --行政区=管城回族区,新郑市,中原区
        python dp_spider_v2/scrap_dp_basic_from_pc.py --城市=郑州市 --行政区=中牟县,高新区,荥阳市,新密市
        python dp_spider_v2/scrap_dp_basic_from_pc.py --城市=郑州市 --行政区=惠济区,巩义市,登封市,郑东新区,上街区
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
    get_dp_comment(城市=城市,行政区=行政区,地区=地区)