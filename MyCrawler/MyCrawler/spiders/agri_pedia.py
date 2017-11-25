import scrapy
from MyCrawler.items import AgriItem

class AgriSpider(scrapy.Spider):
	name = "agri"
	allowed_domains = ["http://agri.ckcest.cn"]
	start_urls = []
	for i in range(0,31000):
		cur = "http://agri.ckcest.cn/agriculturewiki/terminolog/"
		cur = cur + str(i)
		cur = cur + ".html"
		start_urls.append(cur)
#	def __init__(self):
#		self.sum = 0;

	def parse(self, response):		
		# div限定范围
		title_div = response.xpath('//div[@class="termContentBox"]')
		# 获取title
		title = ""
		for p in title_div.xpath('.//h2/text()'):
			title = p.extract().strip()
		
		# div限定范围
		detail_div = response.xpath('//div[@class="termContent"]')
		# 爬取detail内容
		detail = ""
		for p in detail_div.xpath('.//p/text()'):
		    detail = detail + p.extract().strip() + "\n"
		
		# div限定范围
		imageList_div = response.xpath('//div[@class="termContent"]')
		# 爬取imageList内容
		imageList = ""
		for p in imageList_div.xpath(".//p/img/@src"):
			imageList += p.extract().strip() + " "
		
		item = AgriItem()
		item['title'] = title
		item['imageList'] = imageList
		item['detail'] = detail
		item['url'] = response.url
		yield item 