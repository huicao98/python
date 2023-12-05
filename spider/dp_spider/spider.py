from typing import Optional
import re
import time
import random
import logging
import logging.config
import json
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
from .signals import spider_response_processed_singal
from .proxy_pool import ProxyPool
from .browser import BrowserFactory
from .config import CONFIG
from .exceptions import SpiderBlockedException, SpiderExit, SpiderQueryFailException
from .mapper import ShopMapper
from pyquery import PyQuery as pq

global_browser = BrowserFactory.create_browser(config=CONFIG)


class SpiderDataItem:
    def __init__(self, data={}):
        self.data = data


class SpiderDataPipeline:
    def process_item(self, item, spider):
        if isinstance(item, Exception):
            spider.data = item
        else:
            ShopMapper.update_shop(spider.shop)


class SpiderRequest:
    def __init__(self, url, name=None, fetch=None, callback=None):
        self.url = url
        self.fetch = fetch
        self.callback = callback
        self.name = name


class Spider:

    BASIC_URL = 'https://www.baidu.com'

    def __init__(self,
                 id,
                 name='spider',
                 params={},
                 proxy_pool: Optional[ProxyPool] = None):
        self.id = id
        self.name = name
        self.params = params
        self.proxy_pool = proxy_pool
        self.proxy_object = None
        self._browser = None
        self.data = {}
        self.is_closed = False
        self.success = False

    def fetch(self, request):
        self.data = {}

    def start_request(self):
        raise NotImplementedError()

    def parse(self, response, request, *args, **kwargs):
        raise NotImplementedError()

    def create_browser(self):
        self.close_browser()

        if self.proxy_pool:
            self.proxy_object = self.proxy_pool.get_proxy()
            self._browser = BrowserFactory.create_browser(
                self.proxy_object, config=CONFIG)
        else:
            self._browser = BrowserFactory.create_browser(config=CONFIG)

    def close(self):
        """释放

        """
        if not self.is_closed:
            # 代理 放回代理池
            if self.success:
                if self.proxy_pool and self.proxy_object:
                    self.proxy_pool.put_proxy(self.proxy_object)

            self.close_browser()
            self.is_closed = True
            spider_response_processed_singal.send(sender=self)

    def close_browser(self):
        if self._browser:
            try:
                # self._browser.close()
                # self._browser.quit()
                pass
            except:
                pass
            self._browser = None
            pass

    @property
    def browser(self):
        # if not self._browser:
        #     self.create_browser()
        # return self._browser
        return global_browser

    @browser.setter
    def browser(self, value):
        self._browser = value

    @classmethod
    def _sanitize_text(cls, text: str):
        if text:
            text = text.strip()
            # 处理字符串混入html标签
            regex = re.compile(
                r'<(div|span|td)\s*[\w"=\.-]*>[\w\s=+/]*</(div|span|td)\s*\w*>')
            return regex.sub('', text)
        return text

    @classmethod
    def _sanitize_cost(cls, text:str):
        if text:
            text=cls._sanitize_text(text)
            text = text.replace('¥','')
            text = text.replace('￥','')
            text = text.replace('消费：', '')
            text = text.replace('消费:','')
            text = text.replace('元', '')
            text = text.replace('人均','')
            text = text.replace('/人','')
            text = text.replace('-','')
            if text=='':
                text = '0'
            
        return text

    @classmethod
    def random_sleep(cls):
        time.sleep(random.randint(200, 2000)/1000.0)

    @classmethod
    def _get_cookies_as_dict(cls, cookies):
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']
        return cookie_dict


class ShopSpider(Spider):
    def __init__(self,
                 id,
                 shop,
                 name=None,
                 params={},
                 proxy_pool: Optional[ProxyPool] = None):
        super().__init__(id, name, params=params, proxy_pool=proxy_pool)
        self.shop = shop

    def start_request(self):
        url = f'https://www.dianping.com/shop/{self.shop.code}'

        request = SpiderRequest(url,
                                name='shop_info',
                                fetch=self.fetch,
                                callback=self.parse)
        yield request

    def fetch(self, request: SpiderRequest):
        super().fetch(request)
        tries = 0
        response = None
        max_tries = CONFIG.get('max_tries', 3)
        last_ex = None
        while tries < max_tries:
            try:
                self.random_sleep()
                # 重新获取ip查询
                logging.info(f'.....{self.name} {tries+1} 开始查询.....')
                self._request_pc_shop_info_page(request)
                # self._request_mobile_shop_share_page()
                response = True
                break
            except TimeoutException as ex:
                last_ex = ex
                tries += 1
                # logging.info(ex)
            except SpiderBlockedException as ex:
                last_ex = ex
                # 重建 browser
                self.close_browser()
                tries += 1
                # logging.info(ex)
            except WebDriverException as ex:
                last_ex = ex
                # 代理没有作用 或者 chrome配置错误
                tries += 1
                logging.info('代理没有作用 或者 chrome配置错误, 请重新配置!')
                # logging.info(ex)
                self.close_browser()
            finally:
                pass
        if not response:
            if isinstance(last_ex, SpiderBlockedException):
                raise last_ex
            else:
                raise SpiderQueryFailException()
        yield response

    def _request_pc_shop_info_page(self,request):
        # region 从pc端获取详情
        try:
            url = request.url
            self.browser.get('https://www.dianping.com/')
            self.browser.add_cookie({
                        'name':'dper', 'value': CONFIG['dp_dper'],
                    })
            time.sleep(1)
            self.browser.get(url)
            # is_slider = self._is_slider_required()
            # if is_slider:
            #     logging.info('-----find the slider------->')
            #     time.sleep(20)

            # is_login_qr_code = self._is_login_required()
            # if is_login_qr_code:
            #     logging.info('-----find the login qr code------->')
            #     time.sleep(20)

            # 解析查询结果
            # TODO ch 解析内容更详细
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'shop-name'))
            )
            page_source = self.browser.page_source
            doc = pq(page_source)
            if self.shop.city is None:
                cities = doc(".J-current-city")
                if cities:
                    city = self._sanitize_text(cities[0].text)
                    self.shop.city = city

            if self.shop.star is None:
                brief_infos = doc(".brief-info")
                if brief_infos:
                    spans= brief_infos('span')
                    for span in spans.items():
                        if span.attr('class') and 'mid-rank-stars' in span.attr('class'):
                            self.shop.star=span.attr('class')

            if self.shop.name is None:
                names = doc(".shop-name")
                if names:
                    name = self._sanitize_text(names[0].text)
                    self.shop.name = name

            if self.shop.region is None:
                regions = doc("span[itemprop='locality region']")
                if regions:
                    region = self._sanitize_text(regions[0].text)
                    self.shop.region = region

            if self.shop.address is None:
                addresses = doc("span[itemprop='street-address']")
                if addresses:
                    address = self._sanitize_text(addresses[0].text)
                    self.shop.address = address

            if self.shop.cost_avg is None:
                brief_infos = doc(".brief-info")
                if brief_infos:
                    for span in brief_infos[0]:
                        if span.text and '消费' in span.text:
                            cost_avg = self._sanitize_cost(span.text)
                            self.shop.cost_avg = cost_avg

            if self.shop.tel is None:
                tels = doc("span[itemprop='tel']")
                if tels:
                    all_tel = ''
                    for span in tels:
                        tel = self._sanitize_text(span.text)
                        all_tel += tel+','
                    all_tel = all_tel.strip(',')
                    self.shop.tel = all_tel

        except WebDriverException:
            pass
        # endregion
    
    def _request_mobile_shop_share_page(self):
        # region 如果失败再从店面手机分享页面爬数据
        if  not self.shop.is_success():
            mobile_share_url = f'https://m.dianping.com/shopshare/{self.shop.code}?msource=Appshare2021&utm_source=shop_share'
            self.browser.get(mobile_share_url)
            try:
                # case 1
                WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'shopname'))
                )
            except WebDriverException:
                # case 2
                WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'shopName'))
                )
            mobile_page_source = self.browser.page_source
            mobile_doc = pq(mobile_page_source)
                    
            # case 1 https://m.dianping.com/shopshare/GamLG6UWRFE4a5k2?msource=Appshare2021&utm_source=shop_share
            if not self.shop.address:
                mobile_addresses1 = mobile_doc(".i-add")
                if mobile_addresses1:
                    try:
                        mobile_address1 = self._sanitize_text(mobile_addresses1[0].tail)
                        self.shop.address = mobile_address1
                    except:
                        pass

            if not self.shop.star:
                divs = mobile_doc(".component-star:first-child").find('div')
                if divs:
                    for div in divs.items():
                        if div.attr('class') and 'star-score' in div.attr('class'):
                            try:
                                mobile_star = self._sanitize_text(div.text())
                                self.shop.star = mobile_star
                            except:
                                pass

            # case 2 https://m.dianping.com/shopshare/l8sHSfJlKfT4zq7g?msource=Appshare2021&utm_source=shop_share
            if not self.shop.address:
                mobile_addresses2 = mobile_doc(".addressText")
                if mobile_addresses2:
                    mobile_address2 = self._sanitize_text(mobile_addresses2[0].text)
                    self.shop.address = mobile_address2

            
            # case 1 https://m.dianping.com/shopshare/GamLG6UWRFE4a5k2?msource=Appshare2021&utm_source=shop_share
            if  self.shop.cost_avg is None:
                costs1 = mobile_doc(".aver")
                if costs1:
                    try:
                        cost1 = self._sanitize_cost(costs1[0].text)
                        self.shop.cost_avg = cost1
                    except:
                        pass
                            
            # case 2: https://m.dianping.com/shopshare/H7iFIVUmEDXo1DhS?msource=Appshare2021&utm_source=shop_share
            if  self.shop.cost_avg is None:
                costs2 = mobile_doc(".price")
                if costs2:
                    try:
                        self.shop.cost_avg = self._sanitize_cost(costs2[0].text)
                    except:
                        pass

            # case 1 https://m.dianping.com/shopshare/GamLG6UWRFE4a5k2?msource=Appshare2021&utm_source=shop_share
            if not self.shop.tel:
                mobile_tels = mobile_doc("#telphone")
                if mobile_tels:
                    for k,v in dict(mobile_tels[0].items()).items():
                        if k=='href':
                            mobile_tel = self._sanitize_text( v.replace('tel:',''))
                            self.shop.tel = mobile_tel

            # case 2 https://m.dianping.com/shopshare/H7iFIVUmEDXo1DhS?msource=Appshare2021&utm_source=shop_share
            if not self.shop.tel:
                json_cache= json.loads(mobile_doc('body>script')[0].text.replace('window.__xhrCache__ = ',''))
                for k,v in json_cache.items():
                    if 'data' in v and 'phoneNos' in v['data']:
                        tels2 = v['data']['phoneNos']
                        if tels2:
                            mobile_tel2 = ','.join(tels2)
                            self.shop.tel = mobile_tel2

        # endregion
    

    def parse(self, response, request, *args, **kwargs):
        yield SpiderDataItem(data=response)

    def _is_login_required(self):
        try:
            WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'qrcode-img'),))
            qrcode_image = self.browser.find_elements(
                By.CSS_SELECTOR, '.qrcode-img')
            if qrcode_image:
                return True
        except TimeoutException as ex:
            # 没有验证码
            return False
        except NoSuchElementException as ex:
            # 没有验证码
            return False
        return False

    def _is_slider_required(self):
        try:
            WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'puzzle-slider-drag'),))
            slider = self.browser.find_elements(
                By.CSS_SELECTOR, '.puzzle-slider-drag')
            if slider:
                return True
        except TimeoutException as ex:
            # 没有滑块
            return False
        except NoSuchElementException as ex:
            # 没有滑块
            return False
        return False
