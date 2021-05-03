# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class CrawlerPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def open_spider(self, spider):
        print('[+] pipeline start')
        self.f = open('./final6.csv','w')
        self.f.write(f"main_url,main_ip,connect_url,connect_ip,keywords,banner_count\n")

    def close_spider(self, spider):
        print('[+] spider close [+]')
        self.f.close()
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        self.f.write(f"{item['main_url']},{item['main_ip']},{item['connect_url']},{item['connect_ip']},{item['keywords']},{item['banner_count']}\n")
        if self.db_check(item):
            self.store_db(item)
        return item

    def create_connection(self):
        self.conn = sqlite3.connect("final6.db")
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(f"""DROP TABLE IF EXISTS sites_connection""")
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS sites_connection(
                main_url TEXT,
                main_ip TEXT,
                connect_url TEXT,
                connect_ip TEXT,
                keywords TEXT,
                banner_count TEXT
            )
        """
        )

    def store_db(self, item):
        self.cursor.execute(f"""
            INSERT INTO sites_connection VALUES (
                \'{item["main_url"]}\',
                \'{item["main_ip"]}\',
                \'{item["connect_url"]}\',
                \'{item["connect_ip"]}\',
                \'{item["keywords"]}\',
                \'{item["banner_count"]}\'
            )
        """)
        self.conn.commit()
        print(f'[+] db store : {item["main_url"]} {item["connect_url"]}')

    def db_check(self, item):
        sql = f"""
            SELECT 1
            FROM sites_connection
            WHERE main_ip = \'{item["main_ip"]}\' AND connect_ip = \'{item["connect_ip"]}\'
        """ # 조건만족시 1 반환

        result = self.cursor.execute(sql)
        
        return False if len(result.fetchall()) > 0 else True


    


