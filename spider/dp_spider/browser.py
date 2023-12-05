import logging
import logging.config
import os
import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
from fake_useragent import UserAgent

class BrowserFactory:
    @staticmethod
    def create_browser(proxy_object=None,config={}):
        logging.info('>>>>>>>>>>>>>>>创建browser:')
        options = webdriver.ChromeOptions()
        user_agent = UserAgent().random
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        if config.get('headless',True):
            options.add_argument('--headless')
        if config.get('driver_cache',False):
            path = config.get('driver_cache_path')
            size = config.get('driver_cache_size')
            if not os.path.exists(path):
                os.makedirs(path)
            
            options.add_argument(f'--disk-cache-dir={path}')
            options.add_argument(f'--disk-cache-size={size}')

        if config.get('browser_path'):
            options.binary_location=config.get('browser_path')

        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['proxy'] = None
        if proxy_object:
            proxy = Proxy()
            proxy.http_proxy = proxy_object.to_str()
            proxy.ssl_proxy = proxy_object.to_str()
            proxy.add_to_capabilities(capabilities)
            if proxy_object:
                logging.info(proxy_object.to_repr())

        if proxy_object:
            logging.info(proxy_object.to_repr())
            options.add_argument('--proxy-server=%s' % proxy_object.to_str())

        # options.add_argument("--log-level=3")
        browser = webdriver.Chrome(options=options)
        # 防止selenium探测
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                            })
                        """
        })

        browser.delete_all_cookies()
        logging.info(browser.capabilities)

        browser.set_page_load_timeout(100)
        browser.set_window_size(1050, 900)
        return browser
