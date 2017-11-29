import scrapy
from MyCrawler.items import HudongItem
import urllib

split_sign = '##'  # 定义分隔符

class HudongSpider(scrapy.Spider):
	name = "hudong"   #爬虫启动命令：scrapy crawl hudong
	allowed_domains = ["http://www.baike.com"]    #声明地址域
	
	file_object = open('merge_table1.txt','r').read()
	wordList = file_object.split()  # 获取词表
	
	start_urls = []
	count = 0
	for i in wordList:    ##生成url列表
		cur = "http://www.baike.com/wiki/"
		cur = cur + str(i)
		start_urls.append(cur)
		count += 1
		#print(cur)
#		if count > 500:
#			break	

	def parse(self, response):		
		# div限定范围
		main_div = response.xpath('//div[@class="w-990"]')
		
		title = response.url.split('/')[-1]  #  通过截取url获取title
		title = urllib.parse.unquote(title)
		if title.find('isFrom=intoDoc') != -1:
			title = 'error'
		
		url = response.url   # url直接得到
		url = urllib.parse.unquote(url)
		
		img = ""   # 爬取图片url
		for p in main_div.xpath('.//div[@class="r w-300"]/div[@class="doc-img"]/a/img/@src'):
			img = p.extract().strip()
				
		openTypeList = ""  # 爬取开放域标签
		flag = 0   #flag用于分隔符处理（第一个词前面不插入分隔符）
		for p in main_div.xpath('.//div[@class="l w-640"]/div[@class="place"]/p[@id="openCatp"]/a/@title'):
			if flag == 1 :
				openTypeList += split_sign
			openTypeList += p.extract().strip()
			flag = 1
			
		detail = "" # 详细信息
		detail_xpath = main_div.xpath('.//div[@class="l w-640"]/div[@class="information"]/div[@class="summary"]/p')
		if len(detail_xpath) > 0 :   
			detail = detail_xpath.xpath('string(.)').extract()[0].strip()
	
		if detail == "":  # 可能没有
			detail_xpath = main_div.xpath('.//div[@class="l w-640"]/div[@id="content"]')
			if len(detail_xpath) > 0 :   
				detail = detail_xpath.xpath('string(.)').extract()[0].strip()
		
		flag = 0
		baseInfoKeyList = "" #基本信息的key值
		for p in main_div.xpath('.//div[@class="l w-640"]/div[@name="datamodule"]/div[@class="module zoom"]/table//strong/text()'):  
			if flag == 1 :
				baseInfoKeyList += split_sign
			baseInfoKeyList += p.extract().strip()
			flag = 1
			
		flag = 0
		baseInfoValueList = "" #基本信息的value值
		for p in main_div.xpath('.//div[@class="l w-640"]/div[@name="datamodule"]/div[@class="module zoom"]/table//span/text()'):
			if flag == 1 :
				baseInfoValueList += split_sign
			baseInfoValueList += p.extract().strip()
			flag = 1
		
		item = HudongItem()
		item['title'] = title
		item['url'] = url
		item['image'] = img
		item['openTypeList'] = openTypeList
		item['detail'] = detail
		item['baseInfoKeyList'] = baseInfoKeyList
		item['baseInfoValueList'] = baseInfoValueList
				
		yield item 