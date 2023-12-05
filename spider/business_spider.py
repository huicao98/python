import random
import time
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
import openpyxl
from selenium.webdriver.common.action_chains import ActionChains
import requests


class Base:
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--incognito')
        self.driver = webdriver.Chrome(chrome_options=option)
        self.driver.maximize_window()

    def get_driver(self):
        self.driver.get('https://www.dianping.com/')
        time.sleep(1)
        self.driver.add_cookie({
            'name': 'dper',
            'value': 'c233dbbf6968de7fba7b178bf9a32537d1f07ec5474a88e941f880228f7e4e42c9522110f4e988e5d8fbcd100b61c2542e8077363a5e766db06d40078fbe0780',
        })

    def get_url(self,css_style):
        css_style = css_style
        url_match = re.search('url\("([^"]+)"\)', css_style)
        if url_match:
            url = url_match.group(1)
            return url
        else:
            print("URL not found in the CSS style.")

    def run(self):
        self.get_driver()
        workbook = openpyxl.load_workbook("无标题.xlsx")
        # 获取工作表
        sheet = workbook['Sheet1']
        # 读取数据
        data = sheet.iter_rows(min_row=2,values_only=True)
        start_row= 2
        for i in data:
            try:
                print(i)
                if i[8] == '1' or i[8] == 1:
                    start_row += 1
                    continue
                self.driver.get(i[16])
                self.driver.implicitly_wait(2)
                element = self.driver.find_element(By.CSS_SELECTOR,'p.expand-info.tel')
                # 获取电话号码文本
                phone_number = element.text
                addr_ele = self.driver.find_element(By.XPATH, '//*[@id="address"]')
                addr = addr_ele.text
                sheet[f'K{start_row}'] = phone_number
                sheet[f'J{start_row}'] = addr
                star_ele = self.driver.find_element(By.XPATH, '//*[@id="comment_score"]').text
                sheet[f'L{start_row}'] = star_ele
                # ele = self.driver.find_element(By.LINK_TEXT,'食品安全档案')
                # actions = ActionChains(self.driver)
                # actions.move_to_element(ele).perform()
                # ele.click()

                # name_ele = self.driver.find_element(By.XPATH,'//*[@id="shop-tabs"]/div[5]/ul/li[2]')
                # business_name = name_ele.text
                # print(business_name)
                time.sleep(random.randint(1,3))
                # style = self.driver.find_element(By.CLASS_NAME,'licensePic').get_attribute('style')
                # url = self.get_url(style)
                # response = requests.get(url)
                # with open(f'./picture/徐汇区/{i[0]}.png', 'wb') as file:
                #     file.write(response.content)
                # img = openpyxl.drawing.image.Image(f'./picture/烤肉/{i[0]}.png')
                # img.width = img.width * 0.2  # 将宽度减小为原来的一半o
                # img.height = img.height * 0.2  # 将高度减小为原来的一半
                # column = "E"
                # sheet.add_image(img,f"{column}{start_row}")
                # # 调整列宽和行高
                # sheet.column_dimensions[column].width = img.width/5
                # sheet.row_dimensions[start_row].height = img.height
                sheet[f'I{start_row}'] = 1
                workbook.save('无标题.xlsx')
                start_row +=1
            except Exception as e:
                print(e)
                start_row += 1
                continue


if __name__ == '__main__':
    obj = Base()
    obj.run()