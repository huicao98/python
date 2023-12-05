import xlrd
import pymysql
from datetime import datetime
import os
import requests


book = xlrd.open_workbook(f"C:\\Users\\CH\\Desktop\\模板.xlsx")  # 打开需要导入数据库的excel表
sheet = book.sheet_by_name("Sheet1")

# 建立一个MySQL连接
conn = pymysql.connect(
    host='101.132.162.110',
    user='root',
    passwd='5$vyuH^G2ON2Z&0ad$C',
    db='dp_spider',
    port=13306,
    charset='utf8'
)
# 获得游标
cur = conn.cursor()
# 创建插入SQL语句
# id	success	code	name	city	region	cost_avg	tel	address	group_deal	data_source	update_time	create_time
query = 'insert ignore into dp_shop(店名,店铺_详情,人均价格,评价,行政区,地区,菜系,品类,城市,团购,创建时间,更新时间) ' \
        'values (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '
# 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题行
for r in range(1, sheet.nrows):
    店名 = sheet.cell(r, 0).value
    店铺_详情 = sheet.cell(r, 1).value
    人均价格 = sheet.cell(r, 2).value
    评价 = sheet.cell(r, 3).value
    行政区 = sheet.cell(r, 4).value
    地区 = sheet.cell(r, 5).value
    菜系 = sheet.cell(r, 6).value
    品类 = sheet.cell(r, 7).value
    城市 = sheet.cell(r,8).value
    团购 = sheet.cell(r,9).value
    创建时间 = datetime.now()
    更新时间 = datetime.now()
    values = (店名,店铺_详情,人均价格,评价,行政区,地区,菜系,品类,城市,团购,创建时间,更新时间)
    # 执行sql语句
    cur.execute(query, values)
cur.close()
conn.commit()
conn.close()
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print("导入 " + columns + " 列 " + rows + " 行数据到MySQL数据库!")
