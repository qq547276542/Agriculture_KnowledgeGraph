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
    
class HudongItem(scrapy.Item):
    # Item 对应互动百科中的一个词条
    title = scrapy.Field()  #标题
    url = scrapy.Field()  #对于互动百科页面的链接
    image = scrapy.Field()  #图片
    openTypeList = scrapy.Field()  #开放分类列表
    detail = scrapy.Field()  #详细信息
    baseInfoKeyList = scrapy.Field()  #基本信息key列表
    baseInfoValueList = scrapy.Field()  #基本信息value列表
    