import json
import os
import random
import time
from pathlib import Path
import requests
import urllib.parse
import openpyxl
from pprint import pprint


class Base:
    def __init__(self):
        self.cookies = {"accountCenterSessionId":".eJw9jrtqw0AQRf9laxczO7Mvl8EiGCKlSQh2I_YxG1s4ClhODAr598gu0t5zD5wf9TXJuT8WtVaWs7OZdMkxMDqMlDBYH9RK9fUs00GtazxNslL5EMdRTotzlXTDd1_AOQelmsTokayNLuaSOBMbEyUalFwqZo3i_W0NhdCBztWUiMZAsUCskxhe3iwpQMo1GCaNvno0gERZ24BM5AGiJq-dB7EsTJ6WkFGk9FP8lv7y2Zf0HzzdA7uhgf3Lw_F583rZDe9zdwTYb1r99NZw97i9dPP2utMttPNhaD8ao37_ACWBUzQ.F6kMTA.YrTgyWMYWE9IOAIzK4MS77WXnjw"}
        self.Headers = {"Referer":"https://sales.tungee.com/enterprise-details/3762300af03f3452/enterprise-information/basic-information"
                                }

    # 获取公司对应的code
    def get_business_code(self,business_name):
        url = f"https://sales.tungee.com/api/enterprises/search?start=0&end=1&keywords={business_name}&filter=%7B%7D&filter_lead=0&is_canary=1"
        res = requests.get(url,headers = self.Headers,cookies = self.cookies).json()
        return res

    # 获取公司信息
    def get_business_info(self,company_code):
        url = f"https://sales.tungee.com/api/enterprise/info/basic?enterprise_id={company_code}"
        res = requests.get(url,headers = self.Headers,cookies = self.cookies).json()
        return res

    # 获取关联公司信息
    def get_glgs_info(self,human_id):
        url = f"https://sales.tungee.com/api/human/enterprises/filter?human_id={human_id}&history=0&member_type=LEGAL_REPRESENTATIVE&begin=0&end=5"
        res = requests.get(url,headers=self.Headers,cookies=self.cookies).json()
        return res

    # 获取公司联系方式
    def get_company_phone(self,company_code):
        url = f"https://sales.tungee.com/api/lead/contacts?enterprise_id={company_code}&type=company"
        res = requests.get(url,headers=self.Headers, cookies=self.cookies).json()
        return res

    # 获取关联联系方式
    def get_associate_phone(self,company_code):
        url = f"https://sales.tungee.com/api/lead/contacts?enterprise_id={company_code}&type=associate"
        res = requests.get(url, headers=self.Headers, cookies=self.cookies).json()
        return res

    # 获取关键人联系方式
    def get_keylead_phone(self,company_code):
        url = f"https://sales.tungee.com/api/lead/contacts?enterprise_id={company_code}&type=key_lead"
        res = requests.get(url, headers=self.Headers, cookies=self.cookies).json()
        return res

    # 解锁
    def unlock(self,company_code):
        form_data = {"source":"4","enterprise_id":company_code,"entity_type":"enterprise"}
        url = "https://sales.tungee.com/api/lead/unlock"
        requests.put(url,data=form_data, headers=self.Headers, cookies=self.cookies)

    # 高管
    def gg(self,company_code):
        url = f"https://sales.tungee.com/api/enterprise/info/human?enterprise_id={company_code}&position_type=%E9%AB%98%E7%AE%A1&start=0&end=6&key_name="
        res = requests.get(url, headers=self.Headers, cookies=self.cookies).json()
        return res

    def save_as_json(self, company):
        data_dir = os.path.join(os.path.dirname(Path(__file__)), 'data', 'tanji_company')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        print(data_dir)
        company_name = company['name']
        file_name = os.path.join(data_dir, f'{company_name}.json')
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(company, f, ensure_ascii=False, indent=4)

    def run(self):
        workbook = openpyxl.load_workbook("闵行区公司新店.xlsx")
        # 获取工作表
        sheet = workbook['Sheet1']
        data = sheet.iter_rows(min_row=2, values_only=True)
        start_row = 2
        for i in data:

                if i[12] == '1' or i[12] == 1:
                    start_row += 1
                    continue
                time.sleep(random.randint(5, 10))
                url_name = urllib.parse.quote(i[1])
                res = self.get_business_code(url_name)
                print(res)
                # 公司状态
                if res.get("enterprises"):
                    name = res["enterprises"][0].get("name")
                    if name == i[1]:
                        company_stat = res["enterprises"][0].get("operStatus")
                        sheet[f'N{start_row}'] = company_stat
                        company = self.get_company(name)
                        print(company)
                        sheet[f'E{start_row}'] = company["corporate_name"]
                        sheet[f'F{start_row}'] = '\n'.join(company["gj_tels"])
                        sheet[f'G{start_row}'] = '\n'.join(company["gs_tels"])
                        sheet[f'H{start_row}'] = '\n'.join(company["gl_tels"])
                        sheet[f'I{start_row}'] = '\n'.join(company["gg"])
                        sheet[f'J{start_row}'] = '\n'.join(company["gm"])
                        sheet[f'K{start_row}'] = '\n'.join(company["nyye"])
                        if company["glgs"]:
                            for gl_company_name in company["glgs"]:
                                gl_company = self.get_company(gl_company_name, False)
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
                                ii = [i["name"] + ":",
                                      "法人：" + i["corporate_name"],
                                      "关键人联系方式：" + ', '.join(i["gj_tels"]),
                                      "公司联系方式：" + ', '.join(i["gs_tels"]),
                                      "关联联系方式：" + ', '.join(i["gl_tels"])]
                                glgs_text = glgs_text + "\n".join(ii) + "\n"
                            sheet[f'L{start_row}'] = glgs_text
                        sheet[f'M{start_row}'] = '1'
                        self.save_as_json(company)
                        workbook.save('闵行区公司新店.xlsx')
                    start_row += 1
                else:
                    sheet[f'M{start_row}'] = '1'
                    start_row += 1
                    continue

    def get_company(self,company_name,is_getgl_company=True):
        print('正在处理: ', company_name)
        company = {
                "name": "",
                "corporate_name": "",
                "gs_tels": [],
                "gj_tels": [],
                "gl_tels": [],
                "gg": [],
                "glgs": [],
                "glgs_detail": [],
                "gm": "",
                "nyye": ""
        }
        company["name"] = company_name
        url_name = urllib.parse.quote(company_name)
        code_res = self.get_business_code(url_name)

        # 获取公司编码
        company_code = code_res["enterprises"][0].get("_id")
        print("公司编码：",company_code)
        info_res = self.get_business_info(company_code)
        pprint(info_res)

        # 获取法人姓名
        corporate_name = info_res.get("legalRepresentative")
        print("法人：",corporate_name)
        if info_res.get("legalRepresentativeInfo"):
            human_id = info_res.get("legalRepresentativeInfo").get("entity_id")
            print("法人id：",human_id)
        else:
            human_id=""

        company["corporate_name"] = corporate_name

        # 获取年营业额

        nyye = info_res.get("annualTurnoverAlgValueV2")
        if nyye is None:
            nyye = ""
        print("年营业额：",nyye)
        company["nyye"] = nyye

        # 获取规模
        gm = info_res.get("enterpriseScaleAlgValueV2")
        if gm is None:
            gm = ""
        print("公司规模：",gm)
        company["gm"] = gm

        # 解锁
        # 获取关键人联系方式
        keylead_phone_res = self.get_keylead_phone(company_code)
        print("关键人联系方式：",keylead_phone_res)
        if keylead_phone_res.get("contacts"):
            tels = []
            self.unlock(company_code)
            keylead_phone_res = self.get_keylead_phone(company_code)
            keylead_contacts = keylead_phone_res.get("contacts")
            for i in keylead_contacts:
                phone = i.get("contact_label")
                if phone[0] == "1" and len(phone) == 11:
                    phone_desc = i.get("duplicateFamilyName")
                    if phone_desc is None:
                        phone_desc = ""
                    tel = phone+" "+phone_desc
                    print(tel)
                    if tel not in tels:
                        tels.append(tel)
            company["gj_tels"] = tels

        # 解锁
        # 获取公司联系方式
        company_phone_res = self.get_company_phone(company_code)
        print("公司联系方式：",company_phone_res)
        if company_phone_res:
            tels = []
            company_contacts = company_phone_res.get("contacts")
            for i in company_contacts:
                phone = i.get("contact_label")
                print(phone)
                if phone[0] == '1' and len(phone) == 11:
                    # phone_desc = i.get("duplicateFamilyName")
                    self.unlock(company_code)
                    company_phone_res = self.get_company_phone(company_code)
                    company_contacts = company_phone_res.get("contacts")
                    for i in company_contacts:
                        phone = i.get("contact_label")
                        print(phone)
                        if phone[0] == '1' and len(phone) == 11:
                            phone_desc = i.get("duplicateFamilyName")
                            if phone_desc is None:
                                phone_desc = ""
                            tel = phone+ " " +phone_desc
                            print(tel)
                            if tel not in tels:
                                tels.append(tel)
            company["gs_tels"] = tels

        # 获取关联联系方式
        associate_phone_res = self.get_associate_phone(company_code)
        print("关联联系方式：", associate_phone_res)
        if associate_phone_res:
            tels = []
            associate_contacts = associate_phone_res.get("contacts")
            for i in associate_contacts:
                phone = i.get("contact_label")
                print(phone)
                if phone[0] == '1' and len(phone) == 11:
                    phone_desc = i.get("duplicateFamilyName")
                    if phone_desc is None:
                        phone_desc = ""
                    tel = phone + " " + phone_desc
                    print(tel)
                    if tel not in tels:
                        tels.append(tel)
            company["gl_tels"] = tels
        # 获取高管
        gg_res = self.gg(company_code)
        print("高管信息：", gg_res)
        ceos = []
        if gg_res.get("data"):
            for i in gg_res.get("data"):
                gg_name = i.get("humanName")
                ceos.append(gg_name)
            company["gg"] = ceos

        # 获取关联公司
        if is_getgl_company:
            glgs_info_res = self.get_glgs_info(human_id)
            print("关联公司信息：",glgs_info_res)
            guanlianqiyes = []
            glgs_data = glgs_info_res.get("data")
            if glgs_data:
                if len(glgs_data)>4:
                    for i in range(4):
                        glgs_name = glgs_data[i].get("name")
                        if glgs_name != company_name:
                            guanlianqiyes.append(glgs_name)
                else:
                    for i in glgs_data:
                        glgs_name = i.get("name")
                        if glgs_name != company_name:
                            guanlianqiyes.append(glgs_name)
                company["glgs"] = guanlianqiyes
        return company


if __name__ == '__main__':
    obj = Base()
    obj.run()