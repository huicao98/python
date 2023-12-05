import re

import pymysql
from datetime import datetime


ENV= dict(
    host='127.0.0.1',
    user='db_writer',
    passwd='CRzSd&he!OOt3m#JmL5A',
    db='dp_spider',
    port=3306,
    charset='utf8'
)
class Base:
    def __init__(self):
        try:
            # 连接数据库
            self.con = pymysql.connect(host=ENV.get("host"), port=ENV.get("port"),
                                         user=ENV.get("user"), password=ENV.get("passwd"),sql_mode='NO_BACKSLASH_ESCAPES')
            self.cur = self.con.cursor()
        except Exception as e:
            print('数据库连接失败')

    def get_data(self):
        sql = f''' SELECT `店名` ,`点评电话`,`点评地址`,`店铺_详情`, `城市`, `行政区`, `地区`, `品类` FROM dp_spider.dp_shop 
                     WHERE `品类` = '自助餐' AND  `城市` = '上海市' AND `点评电话` is not null AND `点评电话` not like '%添加'
   
                '''
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def filtershops(self,shop):
        filter_shops = ["一品龙虾", "依江宴", "忆宏农家菜", "忆宏饭店宴会厅", "丝路古澜", "农家大锅台", "原物炙泥炉烤肉·烧烤·精酿(吴中路店)", "原物炙烧烤", "练塘农家菜",
                        "壹号地锅", "面舞丝路", "农家地锅（火星店）", "蟹庭丰", "品徽堂", "东北丁家水饺馄饨(南方广场店)", "闯闽堂", "地锅传奇（永平店）",
                        "田老憨老式麻辣烫", "黄子墨功夫煲仔", "T9音乐烤吧", "醉喜厨", "广西老友粉", "福涞海鲜",  "北京片皮烤鸭（新疆故乡烧烤）",
                        "罗记大排档", "胖子海鲜烧烤", "老上海熏鱼", "晓鹅王"]
        for i in filter_shops:
            if i in shop:
                return False
        return True

    def run(self):
        data = self.get_data()
        for i in data:
            print(i)
            res = self.filtershops(i[0])
            if res:
                print(i[1])
                code = i[3].strip('https://www.dianping.com/shop/')
                print(code)
                if ' ' in i[1]:
                    phones = i[1].split(' ')
                else:
                    phones = i[1].split(',')
                print(phones)
                print(len(phones))
                if len(phones) == 1:
                    for phone in phones:
                        phone = phone.strip('电话：\n')
                        phone = phone.strip('[登录显示完整信息]')
                        print(phone)
                        if re.match(r'^\d{11}$',phone) is not None:
                            sql = f''' insert ignore into  dp_spider.crm_customer(客户姓名,手机号码,联系地址,公司名称,来源,唯一标识,城市,区,店铺详情,地区,品类,创建时间)
                                        values ("{i[0]}","{phone}","{i[2]}","{i[0]}","点评","{code}","{i[4]}","{i[5]}","{i[3]}","{i[6]}","{i[7]}","{datetime.now()}")
                                '''
                            print(sql)
                            self.cur.execute(sql)
                            self.con.commit()

                if len(phones) >1:
                    for index,phone in enumerate(phones):
                        print(index,phone)
                        phone = phone.strip('电话：\n')
                        phone = phone.strip('[登录显示完整信息]')
                        if re.match(r'^\d{11}$',phone) is not None:
                            sql = f''' insert ignore into  dp_spider.crm_customer(客户姓名,手机号码,联系地址,公司名称,来源,唯一标识,城市,区,店铺详情,地区,品类,创建时间) 
                                        values ("{i[0]}#{index}","{phone}","{i[2]}","{i[0]}","点评","{code}#{index}","{i[4]}","{i[5]}","{i[3]}","{i[6]}","{i[7]}","{datetime.now()}")
                                '''
                            print(sql)
                            self.cur.execute(sql)
                            self.con.commit()


if __name__ == '__main__':
    obj = Base()
    obj.run()
