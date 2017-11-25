# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
    
class AgriItem(scrapy.Item):
    # Item对应农业百科的一个词条
    title = scrapy.Field()
    imageList = scrapy.Field()
    detail = scrapy.Field()
    url = scrapy.Field()