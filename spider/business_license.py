import json
import os
import base64
import re
import urllib
from datetime import time, datetime
from pathlib import Path

import pymysql
import requests
import csv

API_KEY = "YuWr5N97rh0d9RyqUQHSGdpp"
SECRET_KEY = "7srFqcqLrFZgev4RE7iSYeu4vRwqGdsF"

def main():
        
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/business_license?access_token=" + get_access_token()
    path = './picture/闵行区'
    with open("./data/闵行区2.csv","w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['店名','公司名称','社会信用代码','法人', '成立日期'])
        for filename in os.listdir(path):
            try:
                # image 可以通过 get_file_content_as_base64("C:\fakepath\b2.png",True) 方法获取
                shop_name = filename.split('.')[0]
                filepath = os.path.join(path, filename)
                # print('>> 处理：',filepath)
                payload ='image='+get_file_content_as_base64(filepath,True)
                # print(payload)
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'
                }
                
                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.json())
                create_data = response.json()['words_result']['成立日期']['words']
                corporate = response.json()['words_result']['法人']['words']
                company_name=response.json()['words_result']['单位名称']['words']
                company_code=response.json()['words_result']['社会信用代码']['words']
                time_format_pattern = r'^\d{4}年\d{1,2}月\d{1,2}日$'
                # 使用正则表达式匹配输入的字符串
                if re.match(time_format_pattern, create_data):
                    create_data = create_data
                else:
                    create_data = ""
                data_dir = os.path.join(os.path.dirname(Path(__file__)), 'data', 'dp_company')
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                print(data_dir)
                file_name = os.path.join(data_dir, f'{shop_name}.json')
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=4)
                writer.writerow([shop_name,company_name,company_code,corporate,create_data])
                # conn = pymysql.connect(
                #     host='101.132.162.110',
                #     user='root',
                #     passwd='5$vyuH^G2ON2Z&0ad$C',
                #     db='dp_spider',
                #     port=3306,
                #     charset='utf8'
                # )
                # # 获得游标
                # cur = conn.cursor()
                # # 创建插入SQL语句
                # # id	success	code	name	city	region	cost_avg	tel	address	group_deal	data_source	update_time	create_time
                # query = 'insert ignore into dp_business(店名,公司名,数据详情,品类,创建时间,更新时间) ' \
                #         'values (%s, %s, %s, %s, %s,%s) '
                # # 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题行
                # detail = json.dump(response.json())
                # values = (shop_name,company_name,detail,'烧烤烤串',datetime.now(),datetime.now())
                # # 执行sql语句
                # cur.execute(query, values)
                # cur.close()
                # conn.commit()
                # conn.close()
            except Exception as e:
                print('>> 错误',e)
                continue


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()