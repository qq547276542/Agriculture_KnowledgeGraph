# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
from scrapy.exceptions import DropItem
from scrapy import log

class AgriPipeline(object):
    
    def __init__(self):
        self.count = 0
        self.file = open('MyCrawler/data/agri_economic.json', 'w')
        
    def process_item(self, item, spider):
        if item['title']:
            line = ""
            if(self.count > 0):
                line += ","
            line += json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.file.write(line)
            self.count += 1
            print("count: "+str(self.count))
            return item
        else:
            raise DropItem("忽略无title的组件！")
            
    def open_spider(self, spider):
        self.file.write("[\n")
        print("==================开启爬虫 \""+spider.name+"\" ==================")
        
    def close_spider(self, spider):
        self.file.write("\n]")
        print("==================关闭爬虫 \""+spider.name+"\" ==================")

