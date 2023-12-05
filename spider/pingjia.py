import random
import time
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
import openpyxl


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
            'value': '2b77238bd0188f4205e5c653276f7ddc58d600bdffac76555a9fe1c2747ba72e3e0a55067aabf928e9cdde7b73807ac5b80315db954c73752241247617a58e61',
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
        workbook = openpyxl.load_workbook("数据处理.xlsx")
        # 获取工作表
        sheet = workbook['徐汇区']
        # 读取数据
        data = sheet.iter_rows(min_row=2,values_only=True)
        start_row= 2
        for i in data:
            try:
                print(i)
                if i[17] == '1' or i[17] == 1:
                    start_row += 1
                    continue

                self.driver.get(i[13]+"/review_all")
                self.driver.implicitly_wait(3)
                PageLink = self.driver.find_elements(By.CLASS_NAME,'PageLink')
                print(len(PageLink))
                if len(PageLink)>1:
                    self.driver.get(i[13] + "/review_all"+"/p"+PageLink[-1].text)
                    # self.driver.find_elements(By.CLASS_NAME,'PageLink')[-1].click()
                    first_time = self.driver.find_elements(By.CLASS_NAME,'time')[-1].text
                    sheet[f'R{start_row}'] = 1
                    print(first_time)
                else:
                    first_time = self.driver.find_elements(By.CLASS_NAME, 'time')[-1].text
                    sheet[f'R{start_row}'] = 1
                    print(first_time)
                sheet[f'Q{start_row}'] = first_time
                workbook.save('数据处理.xlsx')
                time.sleep(random.randint(5,7))
                start_row += 1

            except Exception as e:
                print(e)
                start_row += 1
                continue


if __name__ == '__main__':
    obj = Base()
    obj.run()