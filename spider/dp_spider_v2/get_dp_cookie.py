# 获取点评cookie
import os
import time
import random
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
from config import CONFIG,LOGGIN_CONFIG
from browser import BrowserFactory
from mapper import ShopMapper
logging.config.dictConfig(LOGGIN_CONFIG)


from dotenv import find_dotenv, load_dotenv, set_key,get_key
load_dotenv(find_dotenv('local_env'))

def get_cookie(driver=None):
    # driver.delete_cookie('dper')
    # driver.close()
    # driver = None
    if not driver:
        driver = BrowserFactory.create_browser(config={'headless':False,'imageless':False})
    driver.delete_cookie('dper')
    driver.get('https://account.dianping.com/pclogin')
    # driver.get('https://dianping.com/')
    
    time.sleep(2)
    # driver.find_element(By.XPATH,'/html/body/div/div[1]/div[1]/div/div[2]/span[1]/a').click()

    while True:
        print("""!!!!!!!!!!!!!!!
                        !!!!!!! token expired !!!!!!!
                            !!!!!!!!!!!!!""")
                    
        # print( driver.get_cookies())
        for cookie in driver.get_cookies():
            if cookie['name'] =='dper':
                print(f">>> login ok: dper: {cookie['value']}")
                set_key('env','cookie_dper', cookie['value'] )
                return driver
        time.sleep(1)

if __name__ == '__main__':
    # get_cookie()
    set_key('local_env','cookie_dper', 'abssss123' )
    print(get_key('local_env','cookie_dper'))
    print(os.getenv('cookie_dper')) 