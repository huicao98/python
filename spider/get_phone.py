import re
import pandas as pd
import openpyxl

tel_number = r'1\d{10}'  # 通配符，用来匹配单元格内容是符合11位数字的
tel = []  # 构建个存储手机号的列表
workbook = openpyxl.load_workbook("公司-曹辉.xlsx")
# 获取工作表
sheet = workbook['上海自助餐-已处理数据']
min_cell = 'F2'  # 获取范围起始位置
max_cell = 'L596' # 获取范围终止位置
cells = sheet[min_cell:max_cell]
for rows in cells:
    for cell in rows:
        pnumber = re.findall(tel_number, str(cell.value))  # 匹配每个单元格的内容，是否有手机号
        for i in pnumber:
            if i not in tel:
                tel.append(i)
print(tel)
tel = pd.DataFrame(tel)
tel.to_excel(r'C:\Users\CH\Desktop\tel.xlsx')  # 导出文件