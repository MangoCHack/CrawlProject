# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    main_url = scrapy.Field()
    main_ip = scrapy.Field()
    connect_url = scrapy.Field()
    connect_ip = scrapy.Field()
    keywords = scrapy.Field()
    banner_count = scrapy.Field()
    pass
    
