import logging
import logging.config
import os
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
    def create_browser(config={}):
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        if config.get('imageless',True):
            options.add_experimental_option(
                'prefs', {
                'profile.default_content_setting_values': {
                    'images': 2,
                }})
        
        if config.get('headless',True):
            options.add_argument('--headless')
            
        if config.get('driver_cache',False):
            path = config.get('driver_cache_path')
            size = config.get('driver_cache_size')
            if not os.path.exists(path):
                os.makedirs(path)
            
            options.add_argument(f'--disk-cache-dir={path}')
            options.add_argument(f'--disk-cache-size={size}')

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
        browser.set_page_load_timeout(100)
        if config.get('is_max',False):
            browser.maximize_window()
        else:
            browser.set_window_size(1250, 900)

        return browser
