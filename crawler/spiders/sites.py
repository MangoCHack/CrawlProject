# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime as dt
from urllib.parse import urlparse
from util.utils import get_ip, initialize_database, select_all_fullurls, initialize_database2

class SitesPySpider(scrapy.Spider):
    name = 'sites'
    allowed_domains = ['mangacat2.net']
    start_urls = ['https://mangacat2.net/']

    def __init__(self, *args, **kargs):
        today = dt.now().strftime("%Y%m%d")
        
    def start_requests(self):
        dbConnect = initialize_database("illegals.db")
        self.start_urls = select_all_fullurls(dbConnect)
        self.mainIPs = []
        self.tmpStore = {}
        self.dbConnectStore = initialize_database2('sites_connection2.db') # 결과물 DB 저장 초기화
        for url in self.start_urls:
            yield scrapy.Request( url = url, callback= self.link_parse, method='GET', encoding = 'utf=8')
        

    def link_parse(self, response):
        baseIP = get_ip(response.url)
        if baseIP in self.mainIPs:
            yield 0
        self.mainIPs.append(baseIP)
        print(response.url, baseIP)
        links = response.xpath('//a/@href').re(r'http.*') # ToDo : banner link만 수집할 수 있도록 수정
        for link in links:
            try:
                ip = get_ip(link)
                if not self.db_check(self.dbConnectStore, baseIP, ip): # DB 확인 후 같은 노드 없으면 추가
                    row = {'main_url':urlparse(response.url).netloc,'main_ip':baseIP,'connect_url':urlparse(link).netloc,'connect_ip':ip}
                    with self.dbConnectStore:
                        cursor = self.dbConnectStore.cursor()
                        sql = f"""
                            INSERT INTO sites_connection VALUES (
                                \'{row["main_url"]}\',
                                \'{row["main_ip"]}\',
                                \'{row["connect_url"]}\',
                                \'{row["connect_ip"]}\'
                            )
                        """
                        cursor.execute(sql)
                        self.dbConnectStore.commit()
                    print("[+] db store : %s, %s" % (baseIP, ip))
            except Exception as e:
                print(e)
                continue
        yield links

    def link_parse2(self, response): #임시 테스트 결과 메모리저장
        baseIP = get_ip(response.url)
        print(response.url, baseIP)
        links = response.xpath('//a/@href').re(r'http.*')
        for link in links:
            try:
                ip = get_ip(link)
                if (baseIP in self.tmpStore.keys()) and (ip not in self.tmpStore[baseIP]):
                    self.tmpStore[baseIP].append(ip)
                    print("[+] db store : %s, %s" % (baseIP, ip))
                else:
                    self.tmpStore[baseIP] = [ip,]
            except:
                continue
        yield self.tmpStore

    def trace_parse(self, response): #추적
        baseIP = get_ip(response.url)
        print(response.url, baseIP)
        links = response.xpath('//a/@href').re(r'http.*')
        for link in links:
            try:
                ip = get_ip(link)
                if (baseIP in self.tmpStore.keys()) and (ip not in self.tmpStore[baseIP]):
                    self.tmpStore[baseIP].append(ip)
                    print("[+] db store : %s, %s" % (baseIP, ip))
                else:
                    self.tmpStore[baseIP] = [ip,]
            except:
                continue
        yield self.tmpStore

    def db_check(self, dbConnect, mainIP, connectIP):
        try:
            with dbConnect:
                cursor = dbConnect.cursor()

                sql = f"""
                    SELECT 1
                    FROM sites_connection
                    WHERE main_ip = \'{mainIP}\' AND connect_ip = \'{connectIP}\'
                """ # 조건만족시 1 반환

                result = cursor.execute(sql)

                dbConnect.commit()
        except Exception as e:
                print(e)
        return True if len(result.fetchall()) > 0 else False
