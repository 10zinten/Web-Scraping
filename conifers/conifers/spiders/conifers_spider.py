import scrapy
from conifers.items import ConifersItem

class ConiferSpider(scrapy.Spider):
	name = "conifers"
	allowed_domain = ["greatplantpicks.org"]
	start_urls = ["http://www.greatplantpicks.org/plantlists/made_in_the_shade/conifer"]

	# # clones the webpage
	# def parse(self, response):
	# 	filename = response.url.split("/")[-2] + ".html"
	# 	with open(filename, 'wb') as f:
	# 		f.write(response.body)

	# extract name, genus,, species drictly
	def parse(self, response):
		for sel in response.xpath('//tbody/tr'):
			item = ConifersItem()
			item['name'] = sel.xpath('td[@class="common-name"]/a/text()').extract()
			item['genus'] = sel.xpath('td[@class="plantname"]/a/span[@class="genus"]/text()').extract()
			item['species'] = sel.xpath('td[@class="plantname"]/a/span[@class="species"]/text()').extract()
			yield item
