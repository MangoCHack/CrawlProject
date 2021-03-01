# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime as dt
from util.utils import get_ip, initialize_database, select_all_fullurls

class SitesPySpider(scrapy.Spider):
    name = 'sites'
    allowed_domains = ['mangacat2.net']
    start_urls = ['https://mangacat2.net/']

    def __init__(self, *args, **kargs):
        today = dt.now().strftime("%Y%m%d")
        
    def start_requests(self):
        dbConnect = initialize_database("illegals.db")
        self.start_urls = select_all_fullurls(dbConnect)
        #self.start_urls = ['https://mangacat2.net','http://funbe.yoga','http://ww38.bomix2.com','https://copytoon111.com']
        for url in self.start_urls:
            yield scrapy.Request( url = url, callback= self.linkparse, method='GET', encoding = 'utf=8')

    def linkparse(self, response):
        baseIP = get_ip(response.url)
        print(response.url, baseIP)
        links = response.xpath('//a/@href').re(r'http.*')
        ips = []
        for link in links:
            try:
                ip = get_ip(link)
                if (ip is not baseIP) and (ip not in ips): #멀티프로세싱으로 바꾸면 자신의 부모 IP가져오게 만들어야 함
                    ips.append(ip)
                    print(ip, link)
            except:
                continue
        yield ips
