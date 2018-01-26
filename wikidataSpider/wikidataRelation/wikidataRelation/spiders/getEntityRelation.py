import scrapy
import json
import time
import requests
from requests.adapters import HTTPAdapter
from wikidataRelation.items import WikidatarelationItem
class entityRelationSpider(scrapy.spiders.Spider):
	name = "entityRelation"
	allowed_domains = ["wikidata.org"]
	start_urls = [
		"https://www.wikidata.org/w/api.php?action=wbsearchentities&search=abc&language=en"
	]

	def parse(self, response):
		#读取relation及对应的中文名
		entityRelationItem = WikidatarelationItem()
		relationName = dict()
		with open("/home/kuangjun/WikidataSpider/wikidataRelation/relationResult.json", "r") as fr:
			for line in fr.readlines():
				relationJson = json.loads(line)
				relation = relationJson['rmention']
				relationName[relation] = relationJson['chrmention']

		count = 0 
		with open("/home/kuangjun/WikidataSpider/wikidataRelation/readytoCrawl.json","r") as fr:
			for line in fr.readlines():
				count += 1 
				print(1.0*count/33355)
				entityJson  = json.loads(line)
				link = "https:"+entityJson['entity']['url']
				entityName = entityJson['entityOriginName']
				entity = scrapy.Request(link,callback=self.parseEntity)
				entity.meta['entityName'] = entityName
				entity.meta['link'] = link
				yield entity


	def parseEntity(self, response):
		print("=======================")

		entity1 = response.meta['entityName']
		entityRelation = WikidatarelationItem()
		headers = {
			"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
			"accept-language" : "zh-CN,zh;q=0.9,en;q=0.8",
			"keep_alive" : "False"
		}
		for section in response.xpath('//h2[contains(@class,"wb-section-heading")]//span/text()'):
			title = section.extract()
			flag =  0
			if(title == "Statements"):
				flag = 1 
				for statement in response.xpath('.//div[@class="wikibase-statementgroupview"]'):
					relationItem = statement.xpath('.//div[@class="wikibase-statementlistview"]')
					relationName = statement.xpath('.//div[contains(@class,"wikibase-statementgroupview-property-label")]//a[contains(@title,"P")]/text()').extract()
					if(len(relationName)>0):
						relationName = relationName[0]
					else:
						continue
					for relatedEntity in relationItem.xpath('.//div[contains(@class,"wikibase-statementview-mainsnak")]\
						//div[contains(@class,"wikibase-snakview-value-container")]//div[contains(@class,"wikibase-snakview-body")]\
						//div[contains(@class,"wikibase-snakview-value")]//a[contains(@title,"Q")]'):
							entityId = relatedEntity.xpath('./@title').extract()
							if(len(entityId) == 0):
								continue
							else:
								relatedEntityId = entityId[0]							 
								httpRequest = requests.session()
								httpRequest.mount('https://', HTTPAdapter(max_retries=30)) 
								httpRequest.mount('http://',HTTPAdapter(max_retries=30))
								url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+relatedEntityId+"&format=json"
								relatedEntityJson = httpRequest.get(url,headers=headers).json()
								httpRequest.close()
								entity2 = str()
								if 'zh' in relatedEntityJson['entities'][relatedEntityId]['labels']:
									entity2 = relatedEntityJson['entities'][relatedEntityId]['labels']['zh']['value']
								elif 'en' in relatedEntityJson['entities'][relatedEntityId]['labels']:
									entity2 = relatedEntityJson['entities'][relatedEntityId]['labels']['en']['value']
								else:
									continue
								entityRelation['entity1'] = entity1
								entityRelation['relation'] = relationName 
								entityRelation['entity2'] = entity2
								yield entityRelation




						
			if(flag):
				break
		print()
		print("========================")
		#sys.stdout = out
