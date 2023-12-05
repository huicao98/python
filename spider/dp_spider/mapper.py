import pymysql
from pymysql.converters import escape_string
import logging
import typing
from datetime import datetime
from .config import DB_CONFIG


class Shop:
    def __init__(self,
                 id=None,
                 success=0,
                 code=None,
                 name=None,
                 city=None,
                 region=None,
                 cost_avg=None,
                 tel=None,
                 address=None,
                 star=None,
                 data_source=None, *args, **kwargs) -> None:
        self.id = id
        self.success = success
        self.code = code
        self.name = name
        self.city = city
        self.region = region
        self.cost_avg = cost_avg
        self.tel = tel
        self.address = address
        self.star = star
        self.data_source = data_source

    def __repr__(self) -> str:
        return f'id: {self.id} - success: {self.success} - code: {self.code} - name: {self.name} '

    def is_success(self):
        # return self.id != None and self.code != None and self.name != None and self.city != None and self.region != None and self.cost_avg != None and self.tel != None and self.address!=None
        return self.id != None and self.code != None and self.name != None and self.city != None and self.cost_avg != None and self.tel != None and self.address!=None


class ShopMapper:

    @classmethod
    def create_shops(cls, shops: typing.List[Shop]):
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        for shop in shops:
            sql = "insert ignore into shop(success,code,name,data_source,create_time) values(0,'{0}','{1}','{2}','{3}')".format(shop.code,escape_string(shop.店名),shop.data_source,datetime.now())
            logging.info(sql)
            cursor.execute(sql)
            conn.commit()
        cursor.close()
        conn.close()
        return shops

    @classmethod
    def find_all_unsuccess_shops(cls) -> typing.List[Shop]:
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
       SELECT *
FROM shop 
WHERE 状态 = 0 
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(rows)
        shops = []
        for row in rows:
            shop = Shop(**row)
            shops.append(shop)
            logging.info(f'get shop {shop}')

        cursor.close()
        conn.close()
        return shops

    @classmethod
    def update_shop(cls, shop: Shop):

        shop.success = shop.is_success()
        conn = cls._get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"""
             update shop set 状态={shop.success},
            """
        if shop.店名:
            sql += f"""
                店名='{escape_string(shop.name)}',
            """

        # if shop.city:
        #     sql += f"""
        #         city='{shop.city}',
        #     """

        # if shop.region:
        #     sql += f""" region='{shop.region}',
        #     """

        # if shop.cost_avg is not None:
        #     sql += f"""
        #         cost_avg={shop.cost_avg},
        #     """

        if shop.tel:
            sql += f"""
                电话='{shop.tel}',
            """
        if shop.star:
            sql += f"""
                      评分='{shop.star}',
                  """

        if shop.address:
            sql += f"""
                地址='{escape_string(shop.address)}',
            """
        sql += f"""
            update_time = '{datetime.now()}'
            where id={shop.id}
        """
        logging.info(f"shop code: {shop.code} >> {sql}")
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def _get_db_connection(cls):
        return pymysql.connect(**DB_CONFIG)
