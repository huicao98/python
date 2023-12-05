from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from mapper import ShopMapper
from get_dp_cookie import get_cookie

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.dianping.com')
driver = get_cookie(driver=driver)
# driver.add_cookie({
#         'name': 'dper',
#         'value': "333a422b9655210950a143b149e85b7427d284f2b1008a41c1084564fed659426c7aa79f9835e14e9515eb57ad865bcb82faa985fcfd14b8f9513cf1095d2ec8",
#     })
driver.get('https://www.dianping.com/shanghai/ch10/g111c3580')
创建时间 = datetime.now()
更新时间 = datetime.now()
城市 = '上海市'
行政区 = '崇明区'
品类 = '自助餐'
while True:
    list = driver.find_elements(By.XPATH, '//*[@id="shop-all-list"]/ul/li')
    for i in range(1,len(list)+1):
        shop_name = driver.find_element(By.XPATH,f"//*[@id='shop-all-list']/ul/li[{i}]/div[@class='txt']/div[@class='tit']/a[1]").text
        pingjia = driver.find_element(By.XPATH,f"//*[@id='shop-all-list']/ul/li[{i}]/div[@class='txt']/div[@class='comment']/a[1]").text
        renjun = driver.find_element(By.XPATH,f"//*[@id='shop-all-list']/ul/li[{i}]/div[@class='txt']/div[@class='comment']/a[2]").text
        shop_url = driver.find_element(By.XPATH,f"//*[@id='shop-all-list']/ul/li[{i}]/div[@class='txt']/div[@class='comment']/a[2]").get_attribute('href')
        caixi = driver.find_element(By.XPATH,f"//*[@id='shop-all-list']/ul/li[{i}]/div[@class='txt']/div[@class='tag-addr']/a[1]").text
        diqu = driver.find_element(By.XPATH,f"//*[@id='shop-all-list']/ul/li[{i}]/div[@class='txt']/div[@class='tag-addr']/a[2]").text
        try:
            tuangou = driver.find_elements(By.XPATH,f"//body/div[2]/DIV[3]/DIV[1]/DIV[1]/DIV[2]/UL[1]/LI[{i}]/descendant-or-self::DIV[contains(@class,'si-deal d-packup')]//a")
        except Exception:
            pass
        group_deal1 = ''
        for j in range(len(tuangou)):
            tuagou = tuangou[j].get_attribute('title')
            group_deal1 = group_deal1+'@'+str(tuagou)

        values = (shop_name, shop_url, renjun, pingjia, 行政区, diqu, caixi, 品类, 城市,group_deal1, 创建时间, 更新时间)
        ShopMapper.insert_basedata(values)
    try:
        fanye_ele = driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[1]/div[2]/a')
        fanye_ele = fanye_ele[-1]
    except Exception:
            pass
    if '下一页' not in fanye_ele.text:
        break
    else:
        fanye_ele.click()
