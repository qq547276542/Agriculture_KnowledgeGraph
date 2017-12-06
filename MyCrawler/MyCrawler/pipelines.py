# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv
import sys
import time
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


class HudongPipeline(object):   ##用于将hudongItem转化为json，并存到文件中
    
    def __init__(self):
        self.count = 0
        self.file = open('MyCrawler/data/hudong_pedia.json', 'w')
        self.start = time.time()
        
    def process_item(self, item, spider):
        if item['title'] != 'error':   # 'error'是百科中没有的页面赋予的title值（自己定义的）
            line = ""
            if(self.count > 0):
                line += ","
            line += json.dumps(dict(item),ensure_ascii=False) + '\n'
            self.file.write(line)
            self.count += 1
            cur = time.time()
            T = int(cur-self.start)
            print("page count: " + str(self.count) + "      time:" + str(int(T/3600)) + "h " + str(int(T/60)%60) + "m " + str(T%60) + "s......")
            return item
        else:
            raise DropItem("百科中找不到对应页面！")
            
    def open_spider(self, spider):
        self.file.write("[\n")
        print("==================开启爬虫 \""+spider.name+"\" ==================")
        
    def close_spider(self, spider):
        self.file.write("\n]")
        print("==================关闭爬虫 \""+spider.name+"\" ==================")
