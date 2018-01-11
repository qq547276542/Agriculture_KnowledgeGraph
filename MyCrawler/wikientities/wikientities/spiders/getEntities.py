import scrapy
import re
import requests
from wikientities.items import WikientitiesItem
import time
from requests.adapters import HTTPAdapter
class entitiesSpider(scrapy.spiders.Spider):
	name = "entity"
	allowed_domains = ["wikidata.org"]
	start_urls = [
		"https://www.wikidata.org/w/api.php?action=wbsearchentities&search=abc&language=en"
	]
	def containChinese(self,entity):
		zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
		match = zhPattern.search(entity)
		if match:
			return True
		else:
			return False
	def parse(self,response):
		entityList = list()
		entityNumberList = list()
		jsonItemList = list()
		entityCount = 0
		with open('/home/kuangjun/predict_labels7.txt','r') as f:
			for line in f:
				entity = line.split(" ")[0]
				if(len(line.split(" ")) >= 2):
					entityNumber = line.split(" ")[1][0:-1]
				else:
					entityNumber = "999"
				entityList.append(entity)
				entityNumberList.append(entityNumber)
				entityCount += 1
		url_list = list()
		
		count = 0 
		for entity in entityList:
			if(self.containChinese(entity)):
				url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+entity+"&language=zh&format=json"
			else:
				url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+entity+"&language=en&format=json"

			url_list.append(url)


		headers = {
			"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
			"accept-language" : "zh-CN,zh;q=0.9,en;q=0.8",
			"keep_alive" : "False"
		}
		for url in url_list:
			
			print(1.0*count/entityCount)
			#httpRequest = requests.session()
			#httpRequest.keep_alive = False
			httpRequest = requests.session()
			httpRequest.mount('https://', HTTPAdapter(max_retries=30))
			httpRequest.mount('http://', HTTPAdapter(max_retries=30))
			entityjson = httpRequest.get(url,headers=headers).json()
			httpRequest.close()
			entityNumber = str()
			entityOriginName = str()
			if(len(entityNumberList)>count):
				entityNumber = entityNumberList[count]
			else:
				entityNumber = "999"
			if(len(entityList)>count):
				entityOriginName = entityList[count]
			else:
				entityOriginName = "NULL"
			if(len(entityjson['search']) !=0 ):
				tmp = WikientitiesItem()
				tmp['jsonItem'] = entityjson
				tmp['jsonNumber'] = entityNumber
				tmp['entityOriginName'] = entityOriginName
				yield tmp
				jsonItemList.append(tmp)
			count += 1