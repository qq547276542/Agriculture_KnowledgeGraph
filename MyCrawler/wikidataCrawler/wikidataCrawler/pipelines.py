# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
class WikidatacrawlerPipeline(object):
	def __init__(self):
		self.file1 = codecs.open('relation.json','w',encoding = 'utf-8')
		self.file2 = codecs.open('chrmention.json','w',encoding = 'utf-8')

	def process_item(self, item, spider):
		if(item.get('link') is not None):
			line = json.dumps(dict(item),ensure_ascii=False) + '\n'
			self.file1.write(line)
		else:
			line = json.dumps(dict(item),ensure_ascii=False)+'\n'
			self.file2.write(line)
		return item
