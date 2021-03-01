# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime as dt

class SitesPySpider(scrapy.Spider):
    name = 'sites'
    allowed_domains = ['mangacat2.net']
    start_urls = ['https://mangacat2.net/']

    def __init__(self, *args, **kargs):
        today = dt.now().strftime("%Y%m%d")
        
    def start_requests(self):
        self.start_urls = ['https://mangacat2.net/만화책/최신','https://mangacat2.net/포토툰/최신']
        for url in self.start_urls:
            yield scrapy.Request( url = url, callback= self.parse, method='GET', encoding = 'utf=8')

    def parse(self, response):
        contents = response.xpath('//*[@id="wt_list"]/div[1]/div[1]/a')
        
        for content in contents:
            title = content.xpath('a/text()').extract_first()
            item = {
                'title' : title.strip() if title else title
            }
            print(item)
        yield item
