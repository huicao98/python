# 获取点评评论
import os
import time
import random
import threading
import logging
import plyer
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, \
    StaleElementReferenceException
from config import CONFIG, LOGGIN_CONFIG
from browser import BrowserFactory
from mapper import ShopMapper
from get_dp_cookie import get_cookie
from plyer import notification

logging.config.dictConfig(LOGGIN_CONFIG)

from dotenv import find_dotenv, load_dotenv, get_key, set_key

load_dotenv(find_dotenv('local_env'))


class SpiderBlockedException(Exception):
    def __init__(self, message=None):
        super().__init__(message or '被封锁了，请处理')


class SpiderVerifyException(Exception):
    def __init__(self, message=None):
        super().__init__(message or '身份核实，请处理')


def get_dp_comment(a):
    driver = None
    if not driver:
        driver = BrowserFactory.create_browser(config=CONFIG)
    print('driver--->', driver)
    driver.get('https://www.dianping.com/')
    driver = get_cookie(driver=driver)

    # time.sleep(1)
    # driver.add_cookie({
    #         'name': 'dper',
    #         'value': get_key('local_env','cookie_dper'),
    #     })
    # 行政区= [] 代表全部
    # 地区=[] 代表全部
    行政区 = a
    地区 = []

    shops = ShopMapper.find_all_unscrape_basic_or_comment_time_shops(行政区=行政区, 地区=地区)
    while True:
        shops = ShopMapper.find_all_unscrape_basic_or_comment_time_shops(行政区=行政区, 地区=地区)
        if len(shops) == 0:
            logging.info('******任务执行完成啦************')
            break
        try:
            _run_get_dp_comment(shops=shops, driver=driver)
        except SpiderBlockedException as e:
            notification.notify(title="扫码登录", message="点评重新扫码登录", timeout=5)
            get_cookie(driver=driver)
        except SpiderVerifyException as e1:
            pass
            notification.notify(title="身份核验", message="点评身份核验", timeout=5)
        finally:
            pass

    # url = "https://www.dianping.com/shop/G6RhM489G3sYOaNI"
    # review_url = url+"/review_all"
    # driver.execute_script('window.location.href = "{}";'.format(review_url))
    # time.sleep(20)


def _run_get_dp_comment(shops, driver):
    for i, shop in enumerate(shops):
        print(f"total: {len(shops)} no: {i + 1} shop: {shop}")
        url = shop.店铺_详情

        try:
            driver.get(url)
            shop.点评电话 = ''
            shop.点评地址 = ''
            shop.点评评分 = ''
            shop.人均价格 = ''
            shop.评价 = ''
            shop.店铺状态 = '正常营业'
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'shop-name'))
            )
            shopname = driver.find_element(By.CLASS_NAME, 'shop-name')
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

            if shop.是否已获取第一条点评时间 == 2:
                review_url = url + "/review_all"
                driver.get(review_url)
                # case 1
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'review-tabs'))
                )
                page_links = driver.find_elements(By.CLASS_NAME, 'PageLink')
                print(len(page_links))
                first_time = None
                if len(page_links) > 1:
                    driver.get(url + "/review_all" + "/p" + page_links[-1].text)
                    # self.driver.find_elements(By.CLASS_NAME,'PageLink')[-1].click()
                    first_time = driver.find_elements(By.CLASS_NAME, 'time')[-1].text
                else:
                    first_time = driver.find_elements(By.CLASS_NAME, 'time')[-1].text
                if first_time:
                    if '更新于' in first_time:
                        first_time = first_time.split('更新于')[1]
                    shop.第一条点评时间 = first_time
                    ShopMapper.update_shop_basic_and_comment_time(shop)
            else:
                ShopMapper.update_shop_basic_and_comment_time(shop)

        except WebDriverException as e:
            logging.error(f"获取错误1: {e.msg}")
            # 404
            try:
                title = driver.find_element(By.TAG_NAME, 'title')
                if '404 | 大众点评网' in title.text or '404 | 大众点评网' in driver.title:
                    shop.店铺状态 = '商户暂停收录'
                    ShopMapper.update_shop_basic(shop=shop)
                    continue
            except WebDriverException as e5:
                pass

            # 没有评论，不处理
            # 是否评论开放，默认 没有评论时间，否则，判定第一条评论时间是当前时间
            is_comment_ok = False
            if shop.是否已获取第一条点评时间 == 2:
                try:
                    # 评论不展示 https://www.dianping.com/shop/l3nq5BcpgPXMCT7e/review_all
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                        (By.CLASS_NAME, 'not-found-words')))
                    shop.第一条点评时间 = None
                    ShopMapper.update_shop_basic_and_comment_time(shop)
                    logging.error(f'不展示评价：{shop}')
                    is_comment_ok = True
                except Exception as e2:
                    logging.error(f"获取错误2: {e2.msg}")
                    # 没有评论 https://www.dianping.com/shop/laPnlquGggfhNqlP/review_all
                    # 暂不处理
                    try:
                        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-exp')))
                        notice = driver.find_element(By.CLASS_NAME, 'col-exp')
                        if notice.text in '点评和打分都将是其他网友的参考依据，并影响该商户评价。':
                            shop.第一条点评时间 = None
                            ShopMapper.update_shop_basic_and_comment_time(shop)
                            logging.error(f'没有评论：{shop}')
                            is_comment_ok = True

                    except Exception as e3:
                        pass

            try:
                # 是否有滑块
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'dpLogo'))
                )
                logo = driver.find_element(By.CLASS_NAME, "dpLogo").text
                if logo == '身份核实':
                    time.sleep(3)
                    raise SpiderVerifyException()
            except WebDriverException:
                pass

            try:
                if not is_comment_ok:
                    h1 = driver.find_element(By.TAG_NAME, 'h1')
                    if h1.text == '403 Forbidden':
                        # 重新换token
                        logging.error('token expired')

                        print("""!!!!!!!!!!!!!!!
                            !!!!!!! token expired !!!!!!!
                                !!!!!!!!!!!!!""")
                        raise SpiderBlockedException()
            except SpiderBlockedException  as e6:
                raise e6
        except SpiderVerifyException as e5:
            raise e5
        except Exception as e4:
            raise SpiderBlockedException()

        # time.sleep(random.randint(1,3))
    return True


if __name__ == '__main__':

    # 为线程定义一个函数
    class myThread(threading.Thread):
        def __init__(self, x):
            threading.Thread.__init__(self)
            self.x = x

        def run(self):
            get_dp_comment(self.x)


    threads = []

    # 创建新线程

    thread1 = myThread(['三水区', '禅城区', '高明区', '东莞市其他', '中堂镇', '企石镇', '凤岗镇', '南城街道', '厚街镇', '塘厦镇'])
    thread2 = myThread(['南海区', '大朗镇', '寮步镇', '常平镇', '望牛墩镇', '桥头镇', '樟木头镇', '横沥镇', '沙田镇', '清溪镇', '石排镇', '石碣镇'])
    thread3 = myThread(['顺德区', '茶山镇', '莞城街道', '虎门镇', '谢岗镇', '道滘镇', '长安镇', '高埗镇', '麻涌镇', '黄江镇'])

    # 开启新线程
    thread1.start()
    thread2.start()
    thread3.start()

    # 添加新线程到线程列表
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)

    # 等待所有线程完成
    for t in threads:
        t.join()


