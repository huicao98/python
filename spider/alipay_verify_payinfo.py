"""
验证支付宝支付信息
"""
import os
import sys
import json
from pathlib import Path
import random
import time
from selenium import webdriver
import re

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import openpyxl
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(1)

driver.get('https://shenghuo.alipay.com/send/payment/fill.htm?_pdType=afcabecbafgggffdhjch&_tosheet=true')


WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.ID, 'ipt-search-key'))
                )
print('支付宝：输入框已经定位到')

ipt_search_key = driver.find_element(By.ID, 'ipt-search-key')

receive_name_alert = driver.find_element(By.ID,'receiveNameAlert')
receive_name_alert.click()

ipt_search_key.send_keys('18616562780')

receive_name = driver.find_element(By.ID,'receiveNameField')
driver.execute_script("arguments[0].focus();", receive_name)

# 判断是否有错误
time.sleep(1)
try:
    account_status = driver.find_element(By.ID,'accountStatus')
    acccount_status_class = account_status.get_attribute('class')
    print('校验 class:',acccount_status_class)
    if 'ui-tiptext-container ui-tiptext-container-warning' == acccount_status_class:
        print("校验失败：",account_status.text)
    else:
        check_result = ipt_search_key.text
        print("校验成功：", check_result)
except Exception as e:
    print(e)    
    pass

time.sleep(300)
driver.close()
driver.quit()