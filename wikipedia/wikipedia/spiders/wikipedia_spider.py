# from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class WikipediaSpider(CrawlSpider):
	name = "wikipedia"
	allow_domain = ["wikipedia.org"]
	start_urls = [
		"https://en.wikipedia.org/wiki/Mathematics", 
		#"https://en.wikipedia.org/wiki/4"
	]

	rules = [
		Rule(LinkExtractor(restrict_xpaths=['//div[@class="mw-body"]/a/@href'])),
		Rule(LinkExtractor(allow=['https://en.wikipedia.org/wiki/']), callback='parse_item'),
	]

	def parse_item(self, response):
		print response.xpath('//h1[@class="firstHeading"]/text()').extract_first()