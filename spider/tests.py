# # # import threading
# # # import time
# # #
# # # from dp_spider.browser import BrowserFactory
# # # from dp_spider.config import CONFIG
# # #
# # # browser = BrowserFactory.create_browser(config=CONFIG)
# # #
# # # browser.get('https://www.dianping.com/')
# # # time.sleep(1)
# # # browser.add_cookie({
# # #             'name':'dper', 'value':'7110a4d32cba8d6d217be34f1f9e67a8c41578984431ef51898290d87a4fc9d536050babee80403f75891efbbf50be49b289acceb57c0e148ccd81e7ce062bcc',
# # #         })
# # # time.sleep(1)
# # #
# # # browser.get('https://www.dianping.com/shop/G6nWayvhHDvvgsgc')
# # #
# # # time.sleep(2)
# # # browser.get('https://www.dianping.com/shop/l6dlEhibqRIAhvWt')
# # #
# # #
# # # time.sleep(200)
# #
# # import re
# #
# # import time
# # from selenium_utils import build_driver
# #
# #
# # def is_valid_time_format(input_string):
# #     # 定义时间格式的正则表达式
# #     time_format_pattern = r'^\d{4}年\d{1,2}月\d{1,2}日$'
# #
# #     # 使用正则表达式匹配输入的字符串
# #     if re.match(time_format_pattern, input_string):
# #         return True
# #     else:
# #         return False
# #
# # # # 测试
# # # input_str = '年07月31日'
# # # result = is_valid_time_format(input_str)
# # # print(result)  # 输出 True
# #
# # # input_str = '2023年7月31日'
# # # result = is_valid_time_format(input_str)
# # # print(result)  # 输出 True
# #
# # # input_str = '2023-07-31'
# # # result = is_valid_time_format(input_str)
# # # print(result)  # 输出 False
# #
# # def test_build_driver():
# #     driver = build_driver()
# #     driver.get("https://www.baidu.com")
# #     time.sleep(2)
# #
# #
# # if __name__=='__main__':
# #     test_build_driver()
# import threading
# import time
#
#
# class TestThread(threading.Thread):
#     def __init__(self, x):
#         threading.Thread.__init__(self)
#         self.x = x  # 参数接收
#
#     def run(self):
#         time.sleep(self.x)  # 原来的函数写到run中
#         print(str(self.x) + 's')
#
#     def result(self):  # 实现获取调用函数的返回值的方法
#         return self.x
#
#
# t1 = TestThread(1)  # 创建线程
# t2 = TestThread(3)
# t1.start()  # 启动线程
# t2.start()
# t1.join()  # 等待线程结束
# t2.join()
# print(t1.result(), t2.result())
#
# <<<<<<< HEAD
# l1 = ['a','b','c']
# for i in range(0, len(l1), 2):
# 	l2 = l1[i: i + 2]
# 	print(l2)
# =======
# time.sleep(200)

# import re

# import time
# from selenium_utils import build_driver


# def is_valid_time_format(input_string):
#     # 定义时间格式的正则表达式
#     time_format_pattern = r'^\d{4}年\d{1,2}月\d{1,2}日$'

#     # 使用正则表达式匹配输入的字符串
#     if re.match(time_format_pattern, input_string):
#         return True
#     else:
#         return False

# # 测试
# input_str = '年07月31日'
# result = is_valid_time_format(input_str)
# print(result)  # 输出 True

# input_str = '2023年7月31日'
# result = is_valid_time_format(input_str)
# print(result)  # 输出 True

# input_str = '2023-07-31'
# result = is_valid_time_format(input_str)
# print(result)  # 输出 False

# def test_build_driver():
#     driver = build_driver()
#     driver.get("https://www.baidu.com")
#     time.sleep(2)

import tkinter as tk

# 创建主窗口
root = tk.Tk()

# 创建标签和按钮
label = tk.Label(root, text="Hello, Tkinter!")
button = tk.Button(root, text="Click Me!")

# 将标签和按钮添加到主窗口
label.pack()
button.pack()

# 定义按钮点击事件处理函数
def button_click():
    label.config(text="Button Clicked!")

# 将事件处理函数绑定到按钮
button.config(command=button_click)

# 启动Tkinter的主事件循环
root.mainloop()

