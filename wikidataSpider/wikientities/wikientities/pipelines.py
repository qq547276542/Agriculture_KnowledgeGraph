# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
class WikientitiesPipeline(object):
	def __init__(self):
		self.file = codecs.open('entities.json','w',encoding = 'utf-8')


	def process_item(self, item, spider):

		entityjson = json.dumps(dict(item),ensure_ascii=False) + '\n'
		print("pipline")
		print(entityjson)
		self.file.write(entityjson)
		return item
