import tkinter as tk
import threading
from mapper import ShopMapper
import dp_basic_spider


def update_area_options(event):
    selected_city = city_var.get()
    areas = ShopMapper.get_areas(selected_city)
    area_var.set(areas[0] if areas else "")  # 更新区域选择框
    area_menu['menu'].delete(0, 'end')  # 清除旧的选项
    for area in areas:
        area_menu['menu'].add_command(label=area, command=tk._setit(area_var, area))


def start_crawling():
    selected_city = city_var.get()
    selected_area = area_var.get()
    result_label.config(text=f"开始爬取 {selected_city} - {selected_area}")
    crawler_thread = threading.Thread(target=crawl_data, args=(selected_city, selected_area))
    crawler_thread.start()

def crawl_data(city, area):
    areas = []
    areas.append(area)
    # 在这里执行爬虫程序，传递城市和区域作为参数
    dp_basic_spider.get_dp_comment(areas)


root = tk.Tk()
root.title("爬虫控制界面")

cities = ShopMapper.get_cities()
city_label = tk.Label(root, text="选择城市:")
city_var = tk.StringVar()
city_var.set(cities[0] if cities else "")  # 默认选择第一个城市
city_menu = tk.OptionMenu(root, city_var, *cities, command=update_area_options)

area_label = tk.Label(root, text="选择区域:")
area_var = tk.StringVar()
areas = ShopMapper.get_areas(city_var.get())
area_var.set(areas[0] if areas else "")  # 默认选择第一个区域
area_menu = tk.OptionMenu(root, area_var, *areas)

start_button = tk.Button(root, text="开始爬取", command=start_crawling)
result_label = tk.Label(root, text="等待启动")

city_label.pack()
city_menu.pack()
area_label.pack()
area_menu.pack()
start_button.pack()
result_label.pack()

root.mainloop()



