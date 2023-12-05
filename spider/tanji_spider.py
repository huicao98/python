import os
import sys
import json
from pathlib import Path
import random
import time
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
import openpyxl
from selenium.webdriver.common.action_chains import ActionChains


class Base:
    def init(self):
        # option = webdriver.ChromeOptions()
        # option.add_argument("--headless")
        # self.driver = webdriver.Chrome(chrome_options=option)
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(1)

    def login(self):
        self.driver.get('https://user.tungee.com/users/sign-in')
        self.driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[1]/div[1]/div[2]').click()
        self.driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/div[3]/div[2]/section/form/div[1]/div/div/span/span/span/input').send_keys('18348499153')
        self.driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/div[3]/div[2]/section/form/div[2]/div/div/span/span/input').send_keys('YOUtiao123')
        self.driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/div[3]/div[2]/section/form/div[4]/div/div/span/button').click()

    def switch_handle(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def get_phone(self):
        self.driver.find_element(By.XPATH,'//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/div/div[1]/div[4]/span').click()
        time.sleep(1)
        phone_num = phone_num_ele.text
        if phone_num != '手机(0)':
            try:
                self.driver.find_element(By.PARTIAL_LINK_TEXT, '解锁').click()
                time.sleep(1)
            except Exception as e:
                pass
            print(phone_num[3:-1])
            phone_num_ele.click()
            phone_nums = self.driver.find_elements(By.CLASS_NAME, '_2QFKu')
            tels = []
            for i in phone_nums:
                print(i.text)
                tels.append(i.text)

    def run(self):

        workbook = openpyxl.load_workbook("农家菜1501-2475.xlsx")
        # 获取工作表
        sheet = workbook['农家菜1501-2475']
        data = sheet.iter_rows(min_row=2,values_only=True)
        start_row= 2
        companys =[]
        for i in data:
            if i[12] =='1' or i[12]==1:
                start_row += 1
                continue
            self.init()
            self.login()
            print(i)

            self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div[1]/div[2]/div/div/div[2]/div[2]/a[1]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH,'//*[@id="input_search_id"]').send_keys(i[1])
            self.driver.find_element(By.XPATH,'//*[@id="shared_input"]/div/div/ul/li/div/span[1]/span/span[2]/div/div').click()
            business_name =""
            try:
                business_ele = self.driver.find_element(By.XPATH,'//*[@id="find_enterprise_guide_3"]/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[2]/div/section/div[2]/div[1]/h3/a')
                business_name = business_ele.text
            except:
                pass
            if business_name == i[1]:
                try:
                    company_status = self.driver.find_element(By.XPATH,'//*[@id="find_enterprise_guide_3"]/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[2]/div/section/div[2]/div[2]/div').text
                    print('公司状态：',company_status)
                    sheet[f'N{start_row}'] = company_status
                    # if '注销' in company_status:
                    #     start_row += 1
                    #     continue
                except:
                    pass
                business_ele.click()
                self.switch_handle()
                company = self.get_company(business_name)
                sheet[f'E{start_row}'] = company["corporate_name"]
                sheet[f'F{start_row}'] = '\n'.join(company["gj_tels"])
                sheet[f'G{start_row}'] = '\n'.join(company["gs_tels"])
                sheet[f'H{start_row}'] = '\n'.join(company["gl_tels"])
                sheet[f'I{start_row}'] = '\n'.join(company["gg"])
                sheet[f'J{start_row}'] = '\n'.join(company["gm"])
                sheet[f'K{start_row}'] = '\n'.join(company["nyye"])
                if company["glgs"]:
                    for gl_company_href in company["glgs"]:
                        self.driver.get(gl_company_href["href"])
                        time.sleep(1)
                        gl_company=  self.get_company(gl_company_href["name"],False)
                        company["glgs_detail"].append(gl_company)
                # sheet[f'E{start_row}'] = company["corporate_name"]
                # sheet[f'F{start_row}'] = '\n'.join(company["gj_tels"])
                # sheet[f'G{start_row}'] = '\n'.join(company["gs_tels"])
                # sheet[f'H{start_row}'] = '\n'.join(company["gl_tels"])
                # sheet[f'I{start_row}'] = '\n'.join(company["gg"])
                # sheet[f'J{start_row}'] = '\n'.join(company["gm"])
                # sheet[f'K{start_row}'] = '\n'.join(company["nyye"])
                    glgs_text = ""
                    for i in company["glgs_detail"]:
                        ii = [i["name"]+":",
                              "法人："+i["corporate_name"],
                              "关键人联系方式："+', '.join(i["gj_tels"]),
                              "公司联系方式："+', '.join(i["gs_tels"]),
                              "关联联系方式："+', '.join(i["gl_tels"])]
                        glgs_text = glgs_text+ "\n".join(ii)+"\n"
                    sheet[f'L{start_row}'] = glgs_text
                status_column = 'M'
                sheet[f'{status_column}{start_row}'] = '1'

                # time.sleep(500)
                self.save_as_json(company)
                workbook.save('农家菜1501-2475.xlsx')
                self.driver.quit()
                time.sleep(1)
            start_row += 1

        # time.sleep(10)
    def get_company(self,company_name,is_getgl_company=True):
        print('正在处理: ',company_name)
        company = {
            "name": "",
            "corporate_name": "",
            "gs_tels": [],
            "gj_tels": [],
            "gl_tels": [],
            "gg": [],
            "glgs": [],
            "glgs_detail":[],
            "gm": "",
            "nyye": "",
        }
        company["name"] = company_name
        try:
            corporate_ele = self.driver.find_element(By.XPATH, '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[1]/div[2]/section/div[1]/span[1]')
            corporate_name = corporate_ele.text
            print(corporate_name)
            company["corporate_name"] = corporate_name
        except:
            print("法人信息提取错误：",company_name)
        # cor_column = 'E'
        # sheet[f'{cor_column}{start_row}'] = corporate_name
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/div/div[1]/div[4]/span').click()
        time.sleep(1)

        gs_phone_num_ele = None
        try:
            gs_phone_num_ele = self.driver.find_element(By.XPATH,
                                                    '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/label[2]/span[2]')
        except:
            try:
                gs_phone_num_ele = self.driver.find_element(By.XPATH,
                                                        '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/label[2]')
            except:
                pass

        if gs_phone_num_ele:
            gs_phone_num = gs_phone_num_ele.text
            if gs_phone_num != '手机(0)':
                try:
                    # 解锁
                    #
                    ele = self.driver.find_elements(By.XPATH,'//button')
                    for i in ele:
                        if i.text == '解锁':
                            i.click()
                            break

                    time.sleep(1)
                except Exception as e:
                    pass


        lianxiren_tabs = self.driver.find_elements(By.XPATH,
                                                   '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div/div[1]/child::div')

        if len(lianxiren_tabs)>0:
            for tab in lianxiren_tabs:
                text = tab.text
                if '关键人联系方式' in text:
                    try:
                        # 解锁
                        ele = self.driver.find_elements(By.XPATH, '//button')
                        for i in ele:
                            if i.text == '解锁':
                                i.click()
                                break
                        # self.driver.find_element(By.XPATH, '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div[3]/p[2]/button').click()
                        time.sleep(1)
                    except Exception as e:
                        pass

        if len(lianxiren_tabs)>0:
            for tab in lianxiren_tabs:
                text = tab.text
                print(text)
                if '公司联系方式' in text:
                    try:
                        print('进入了公司联系方式')
                        # tab.click()
                        gs_phone_num_ele.click()
                        phone_nums = self.driver.find_elements(By.CLASS_NAME, '_2lVpt')
                        tels = []
                        for i in phone_nums:
                            if i.text[0] == '1':
                                print(i.text)
                                tels.append(i.text)
                        company["gs_tels"] = tels
                        print('公司联系方式所有号码: ', tels)
                        # gs_phone_column = 'G'
                        # sheet[f'{gs_phone_column}{start_row}'] = '\n'.join(tels)
                    except Exception as e:
                        pass
                if '关键人联系方式' in text:
                    try:
                        # self.driver.find_element(By.PARTIAL_LINK_TEXT, '关键人联系方式').click()
                        # print('已点击：关键人联系方式')
                        tab.click()
                        print('已点击：关键人联系方式')
                        time.sleep(1)
                        self.driver.find_element(By.XPATH,
                                                 '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/label[2]/span[2]').click()
                        phone_nums = self.driver.find_elements(By.CLASS_NAME, '_2lVpt')
                        tels = []
                        for i in phone_nums:
                            if i.text[0] == '1':
                                print(i.text)
                                tels.append(i.text)
                        company["gj_tels"] = tels
                        print('关键人联系方式所有号码: ', tels)
                        # gj_phone_column = 'F'
                        # sheet[f'{gj_phone_column}{start_row}'] = '\n'.join(tels)
                    except Exception as e:
                        pass
                if '关联联系方式' in tab.text:
                    try:
                        # print('开始点击：关联联系方式')
                        # self.driver.find_element(By.PARTIAL_LINK_TEXT, '关联联系方式').click()
                        tab.click()
                        print('已点击：关联联系方式')
                        time.sleep(1)
                        self.driver.find_element(By.XPATH,
                                                 '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div[3]/div[1]/div/label[2]/span[2]').click()
                        phone_nums = self.driver.find_elements(By.CLASS_NAME, '_2lVpt')
                        tels = []
                        for i in phone_nums:
                            if i.text[0] == '1':
                                print(i.text)
                                tels.append(i.text)
                        company["gl_tels"] = tels
                        print('关联联系方式所有号码: ', tels)
                        # gl_phone_column = 'H'
                        # sheet[f'{gl_phone_column}{start_row}'] = '\n'.join(tels)
                    except Exception as e:
                        pass
        else:
            try:
                print('进入了公司联系方式')
                gs_phone_num_ele.click()
                phone_nums = self.driver.find_elements(By.CLASS_NAME, '_2lVpt')
                tels = []
                for i in phone_nums:
                    if i.text[0] == '1':
                        print(i.text)
                        tels.append(i.text)
                company["gs_tels"] = tels
                print('公司联系方式所有号码: ', tels)
            except Exception as e:
                pass

        try:
            year_value_ele = self.driver.find_element(By.XPATH,
                                                      '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[1]/div[2]/section/div[1]/span[3]')
            year_value = year_value_ele.text
            if "人员规模" in year_value or "年营业额" in year_value:
                company["nyye"] = year_value
            else:
                company["nyye"] = ""
            print(year_value)
            # year_value_column = 'I'
            # sheet[f'{year_value_column}{start_row}'] = year_value
        except Exception as e:
            pass

        try:
            gm_ele = self.driver.find_element(By.XPATH,
                                              '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[1]/div[2]/section/div[1]/span[2]')
            gm = gm_ele.text
            print(gm)
            if "人员规模" in gm or "年营业额" in gm:
                company["gm"] = gm
            else:
                company["gm"]=""
            # year_value_column = 'J'
            # sheet[f'{year_value_column}{start_row}'] = year_value
        except Exception as e:
            pass
        try:
            self.driver.find_element(By.XPATH,
                                     '//*[@id="enterprise-details"]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/div/div[1]/div[5]/span').click()
            ele = self.driver.find_element(By.XPATH, '//*[@id="ceo"]/parent::*')
            print(ele.text[2:])
            ele1 = self.driver.find_elements(By.CLASS_NAME, 'XlVF6')
            ceos = []
            for i in range(int(ele.text[2:])):
                ceos.append(ele1[i].text)
            company["gg"] = ceos
            # ceo_column = 'K'
            # sheet[f'{ceo_column}{start_row}'] = '\n'.join(ceos)
        except Exception as e:
            pass

        if is_getgl_company:
            try:
                ele = self.driver.find_elements(By.CLASS_NAME, '_2bW4A')[0].get_attribute('href')
                print(ele)
                self.driver.get(ele)
                time.sleep(1)
                guanlianqiye = self.driver.find_elements(By.CSS_SELECTOR, '.pqf1J > a')
                guanlianqiyes = []
                guanlianqiye_hrefs = set()
                if len(guanlianqiye) > 4:
                    for i in range(4):
                        print('关联企业大于4')
                        print(guanlianqiye[i].get_attribute('href'))
                        guanlianqiye_href = guanlianqiye[i].get_attribute('href')
                        guanlianqiye_name = guanlianqiye[i].text
                        if guanlianqiye_name != company_name:
                            if guanlianqiye_href not in guanlianqiye_hrefs:
                                guanlianqiye_hrefs.add(guanlianqiye_href)
                                guanlianqiyes.append({"name": guanlianqiye_name, "href": guanlianqiye_href})
                else:
                    for i in guanlianqiye:
                        print('关联企业小于4')
                        guanlianqiye_href = i.get_attribute('href')
                        guanlianqiye_name = i.text
                        if guanlianqiye_name != company_name:
                            if guanlianqiye_href not in guanlianqiye_hrefs:
                                guanlianqiye_hrefs.add(guanlianqiye_href)
                                guanlianqiyes.append({"name": guanlianqiye_name, "href": guanlianqiye_href})
                print('关联企业全部链接： ', guanlianqiyes)
                company["glgs"] = guanlianqiyes
            except Exception as e:
                pass
        return company
    
    def save_as_json(self, company):
        data_dir = os.path.join(os.path.dirname(Path(__file__)), 'data', 'tanji_company')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        print(data_dir)
        company_name = company['name']
        file_name = os.path.join(data_dir, f'{company_name}.json')
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(company, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    obj = Base()
    obj.run()
