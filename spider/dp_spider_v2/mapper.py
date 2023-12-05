import pymysql
from pymysql.converters import escape_string
import logging
import typing
from datetime import datetime
from config import DB_CONFIG


class Shop:
    def __init__(self,
                 id=None,
                 店名=None,
                 行政区=None,
                 地区=None,
                 人均价格=None,
                 评价=None,
                 菜系=None,
                 品类=None,
                 是否获取点评基础数据=None,
                 点评地址=None,
                 点评电话=None,
                 点评评分=None,
                 是否已获取第一条点评时间=None,
                 第一条点评时间=None,
                 是否已解析证照=None,
                 证照_公司成立时间=None,
                 证照数据=None,
                 店铺_详情=None,
                 店铺状态 = None,
                连锁店数量=0, *args, **kwargs) -> None:
        self.id = id
        self.店名 = 店名
        self.行政区 = 行政区
        self.地区 = 地区
        self.人均价格 = 人均价格
        self.评价 = 评价
        self.菜系 = 菜系
        self.品类 = 品类
        self.是否获取点评基础数据 = 是否获取点评基础数据
        self.点评地址 = 点评地址
        self.点评电话 = 点评电话
        self.点评评分 = 点评评分
        self.是否已获取第一条点评时间 = 是否已获取第一条点评时间
        self.第一条点评时间 = 第一条点评时间
        self.是否已解析证照 = 是否已解析证照
        self.证照_公司成立时间 = 证照_公司成立时间
        self.店铺_详情 = 店铺_详情
        self.证照数据 = 证照数据
        self.店铺状态 = 店铺状态
        self.连锁店数量 = 连锁店数量

    @property
    def code(self):
        return self.店铺_详情.split('/')[-1]

    def __repr__(self) -> str:
        return f'id: {self.id} - 店名: {self.店名} url: {self.店铺_详情} code: {self.code} 点评电话：{self.点评电话} 人均价格: {self.人均价格} 点评评分: {self.点评评分} 评价: {self.评价} 点评地址：{self.点评地址} 第一条点评时间：{self.第一条点评时间}'

class ShopMapper:
    # 获取所有的点
    @classmethod
    def find_all_shops(cls) -> typing.List[Shop]:
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
         SELECT * FROM dp_shop
        """
        
        logging.info('sql>> %s', sql)

        cursor.execute(sql)
        rows = cursor.fetchall()
        shops = []
        for row in rows:
            shop = Shop(**row)
            shops.append(shop)

        cursor.close()
        conn.close()
        return shops

    # 更新连锁店的数量
    @classmethod
    def update_chain_count(cls, shop):
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        match_name = shop.店名[0:5].replace("'","")
        if "(" in match_name:
            match_name = shop.店名.split("(")[0]
        sql = f"""
             update dp_shop set 连锁店数量= ( select c from( select count(*) as c from dp_shop b where b.店名 like '{match_name}%') d )
                where id={shop.id}
        """
        logging.info('sql>> %s', sql)

        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        
    
    # 批量更新连锁店的数量
    @classmethod
    def batch_update_chain_count(cls, shops):
        conn = cls._get_db_connection()

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        batch_sql = ''
        
        for shop in shops:
            match_name = shop.店名[0:5].replace("'","").replace(")","").replace("(","")
            sql = f"""update dp_shop set 连锁店数量= ( select c from( select count(*) as c from dp_shop b where b.店名 like '{match_name}%') d )
                    where id={shop.id};"""
            batch_sql+=sql
            cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        conn.close()
    # @classmethod
    # def batch_update_chain_count2(cls, shops):
    #     batch_sql = ''
        
    #     for shop in shops:
    #         match_name = shop.店名[0:5].replace("'","")
    #         if "(" in match_name:
    #             match_name = shop.店名.split("(")[0]

    #         sql = f"""update dp_shop set 连锁店数量= ( select c from( select count(*) as c from dp_shop b where b.店名 like '{match_name}%') d )
    #                 where id={shop.id};"""
    #         batch_sql+=sql

    #     logging.info('batch_sql>> %s', batch_sql)
    #     from sqlalchemy import create_engine
    #     from sqlalchemy import text

    #     engine = create_engine(f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    #     with engine.connect() as connection:
    #         connection.execute(text(batch_sql))

    @classmethod
    def batch_update_chain_count2(cls):
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'CALL `proce_shop_chain_num`()'
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    # 获取所有没有获取点评基础数据或评论时间的店铺
    @classmethod
    def find_all_unscrape_basic_or_comment_time_shops(cls,行政区=[],地区=[]) -> typing.List[Shop]:
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
         SELECT * FROM dp_shop WHERE (`是否已获取第一条点评时间` = 0 or `是否获取点评基础数据` = 0) 
        """
        if len(行政区)>0:
            condition = "'"+"','".join(行政区)+"'"
            sql += f" and `行政区` in ({condition})"
        
        if len(地区)>0:
            condition = "'"+"','".join(地区)+"'"
            sql += f" and `地区` in ({condition})"
        
        logging.info('sql>> %s', sql)

        cursor.execute(sql)
        rows = cursor.fetchall()
        shops = []
        for row in rows:
            shop = Shop(**row)
            shops.append(shop)
            # logging.info(f'get shop {shop}')

        cursor.close()
        conn.close()
        return shops

    # 更新点评基础数据和评论时间
    @classmethod
    def update_shop_basic_and_comment_time(cls, shop: Shop):
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if shop.第一条点评时间:
            sql = f"""
                update dp_shop set `第一条点评时间`='{shop.第一条点评时间}',
                `是否已获取第一条点评时间`=1,
                `更新时间` = '{datetime.now()}',
                点评电话 = '{shop.点评电话}',
                点评地址='{shop.点评地址}',
                点评评分='{shop.点评评分}',
                人均价格='{shop.人均价格}',
                评价='{shop.评价}', 
                店铺状态 = '{shop.店铺状态}',
                是否获取点评基础数据 = 1
                where id={shop.id}
                """
        else:
            sql = f"""
             update dp_shop set `第一条点评时间`=null,
             `是否已获取第一条点评时间`=1,
            `更新时间` = '{datetime.now()}',
            点评电话 = '{shop.点评电话}',
            点评地址='{shop.点评地址}',
            点评评分='{shop.点评评分}',
            人均价格='{shop.人均价格}',
            评价='{shop.评价}', 
            店铺状态 = '{shop.店铺状态}',
            是否获取点评基础数据 = 1
            where id={shop.id}
            """
              
        logging.info(f"shop: {shop} >> {sql}")
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    # 获取所有没有获取点评基础数据的店铺
    @classmethod
    def find_all_unscrape_basic_shops(cls,城市=[],行政区=[],地区=[]) -> typing.List[Shop]:
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
         SELECT * FROM dp_shop WHERE `是否获取点评基础数据` = 0
        """

        if len(城市)>0:
            condition = "'"+"','".join(城市)+"'"
            sql += f" and `城市` in ({condition})"

        if len(行政区)>0:
            condition = "'"+"','".join(行政区)+"'"
            sql += f" and `行政区` in ({condition})"
        
        if len(地区)>0:
            condition = "'"+"','".join(地区)+"'"
            sql += f" and `地区` in ({condition})"
        
        logging.info('sql>> %s', sql)

        cursor.execute(sql)
        rows = cursor.fetchall()
        shops = []
        for row in rows:
            shop = Shop(**row)
            shops.append(shop)
            # logging.info(f'get shop {shop}')

        cursor.close()
        conn.close()
        return shops
    
    # 更新点评基础数据
    @classmethod
    def update_shop_basic(cls, shop: Shop):
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if shop.第一条点评时间:
            sql = f"""
                update dp_shop set
                `更新时间` = '{datetime.now()}',
                点评电话 = '{shop.点评电话}',
                点评地址="{shop.点评地址}",
                点评评分='{shop.点评评分}',
                人均价格='{shop.人均价格}',
                评价='{shop.评价}', 
                店铺状态 = '{shop.店铺状态}',
                是否获取点评基础数据 = 1
                where id={shop.id}
                """
        else:
            sql = f"""
             update dp_shop set
            `更新时间` = '{datetime.now()}',
            点评电话 = '{shop.点评电话}',
            点评地址='{shop.点评地址}',
            点评评分='{shop.点评评分}',
            人均价格='{shop.人均价格}',
            评价='{shop.评价}', 
            店铺状态 = '{shop.店铺状态}',
            是否获取点评基础数据 = 1
            where id={shop.id}
            """
              
        logging.info(f"shop: {shop} >> {sql}")
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()


    # 获取所有没有获取点评评论时间的店铺
    @classmethod
    def find_all_unscrape_comment_time_shops(cls,行政区=[],地区=[]) -> typing.List[Shop]:
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
         SELECT * FROM dp_shop WHERE  `是否已获取第一条点评时间` =0
        """
        if len(行政区)>0:
            condition = "'"+"','".join(行政区)+"'"
            sql += f" and `行政区` in ({condition})"
        
        if len(地区)>0:
            condition = "'"+"','".join(地区)+"'"
            sql += f" and `地区` in ({condition})"
        
        logging.info('sql>> %s', sql)

        cursor.execute(sql)
        rows = cursor.fetchall()
        shops = []
        for row in rows:
            shop = Shop(**row)
            shops.append(shop)
            # logging.info(f'get shop {shop}')

        cursor.close()
        conn.close()
        return shops

    # 更新点评第一条点评时间
    @classmethod
    def update_shop_comment_time(cls, shop: Shop):
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if shop.第一条点评时间:
            sql = f"""
                update dp_shop set `第一条点评时间`='{shop.第一条点评时间}',
                `是否已获取第一条点评时间`=1,
                `更新时间` = '{datetime.now()}'
                where id={shop.id}
                """
        else:
            sql = f"""
             update dp_shop set `第一条点评时间`=null,
             `是否已获取第一条点评时间`=1,
            `更新时间` = '{datetime.now()}'
            where id={shop.id}
            """
              
        logging.info(f"shop: {shop} >> {sql}")
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    # 查询需要获取电话的城市
    @classmethod
    def get_cities(cls):
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = ''' select distinct `城市` from dp_shop where `是否获取点评基础数据` = 0
                '''
        cursor.execute(sql)
        rows = cursor.fetchall()
        cities = []
        for row in rows:
            print(row)
            city = row.get('城市')
            cities.append(city)
        return cities

    # 查询需要获取电话的行政区
    @classmethod
    def get_areas(cls,city):
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f''' select distinct `行政区` from dp_shop where 城市 = '{city}' and `是否获取点评基础数据` = 0
                '''
        cursor.execute(sql)
        rows = cursor.fetchall()
        regions = []
        for row in rows:
            print(row)
            region = row.get('行政区')
            regions.append(region)
        return regions

    # 插入基础数据
    @classmethod
    def insert_basedata(cls,values):
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """insert ignore into dp_shop(店名,店铺_详情,人均价格,评价,行政区,地区,菜系,品类,城市,团购,创建时间,更新时间) 
        values (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,values)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def _get_db_connection(cls):
        return pymysql.connect(**DB_CONFIG)
