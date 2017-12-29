import scrapy
import time
import re
from wikidataCrawler.items import WikidatacrawlerItem
from scrapy_splash import SplashRequest
class relationSpider(scrapy.spiders.Spider):
	name = "relation"
	allowed_domains = ["wikidata.org"]
	start_urls = [
		"https://www.wikidata.org/wiki/Wikidata:List_of_properties/Summary_table"

	]
	def parse(self , response):
		count = 0 
		rcount = 0 
		relationItem_list = list()
		relationType = list()
		link_list = list()
		rtype_list = list()
		for headline in response.xpath('//span[contains(@class,"mw-headline")]'):
			rtype = re.sub("[^A-Za-z]","",headline.xpath('.//text()').extract()[0])
			rtype_list.append(rtype)
		table_number_list = [5,7,9,2,14,20,13,5]
		rcount = 1
		rrcount = 0
		rrrcount = 0 
		for table in response.xpath('//table[contains(@class,"wikitable")]'):
			rsubtype = re.sub("[^A-Za-z\s]","",table.xpath('.//th/text()').extract()[0])
			for li in table.xpath('.//li/a'):
				relationId = li.xpath('./small/text()').extract()[0]
				relationId = re.sub("[^A-Za-z0-9]","",relationId)
				link = li.xpath('./@href').extract()[0]
				link = re.sub("[[]\']","",link)
				link = "https://www.wikidata.org"+link
				link_list.append(link)
				rmention = li.xpath('.//text()').extract()[0]
				rmention = re.sub("[^A-za-z0-9\s]","",rmention)
				if((rtype_list[rcount] == 'Organization' and rsubtype == 'Generic') or(rtype_list[rcount] == 'Works' and rsubtype == 'Film')):
					continue
				tmp  =WikidatacrawlerItem()
				relationItem_list.append(WikidatacrawlerItem())
				relationItem_list[count]['rid'] = relationId
				relationItem_list[count]['rtype'] = rtype_list[rcount]
				relationItem_list[count]['rsubtype'] = rsubtype
				relationItem_list[count]['link'] = link
				relationItem_list[count]['rmention'] = rmention
				yield relationItem_list[count]
				count+=1
			rrrcount += 1
			if(rrrcount == table_number_list[rrcount] ):
				rrrcount = 0 
				rrcount += 1
				rcount += 1
				
		print('number of relation types is %d'  %count)
		splash_args = {
            'wait': 0.5,
        }
		for url in link_list:
			chrelationItem = WikidatacrawlerItem()
			request = scrapy.Request(url, callback=self.parse_relation_pages)
			request.meta['item'] = chrelationItem
			rid = url.split(":")[2]
			request.meta['rid'] = rid
			yield request



	def parse_relation_pages(self , response):
		chrelationItem = response.meta['item']
		chrelationItem['rid'] = response.meta['rid']		
		zh_pattern = re.compile(r'\\\"language\\\":\\\"zh\\\",\\\"value\\\":\\\"(.*?)\\\"')
		zhhans_pattern = re.compile(r'\\\"language\\\":\\\"zh-hans\\\",\\\"value\\\":\\\"(.*?)\\\"')
		for script in response.xpath('//script').extract():
			zh = re.findall(zh_pattern,script)
			if(len(zh)>0):
				zh[0] = re.sub(r'\\\\',r'\\',zh[0])
				chrelationItem['chrmention'] = zh[0].encode('latin-1').decode('unicode_escape')
				break;
				
			else:
				zh_hans = re.findall(zhhans_pattern,script)
				if(len(zh_hans) > 0 ):

					zh_hans[0] = re.sub(r'\\\\',r'\\',zh_hans[0])				
					chrelationItem['chrmention'] = zh_hans[0].encode('latin-1').decode('unicode_escape')
					break;
				else:
					chrelationItem['chrmention'] = "no chinese label"
		return chrelationItem

