import re
import scrapy
from Imdb.items import MovieItem, CastItem

class ImdbSpider(scrapy.Spider):
	name = "imdb"
	allow_domains = ["imdb.com"]
	start_urls = [
		# Top 250 list of English movies
		"http://www.imdb.com/chart/top?ref_=nv_ch_250_4",
	]

	# parsing the top 250 IMDB page and doing the callback request to each title link
	def parse(self, response):
		# self.wanted_num = 10
		for sel in response.xpath('//table[@class="chart full-width"]/tbody/tr'):
			item = MovieItem()
			item['title'] = sel.xpath('td[2]/a/text()').extract_first()
			item['rating'] = sel.xpath('td[3]/strong/text()').extract_first()
			item['ranking'] = sel.xpath('td[1]/span[1]/@data-value').extract_first()
			item['release_year'] = sel.xpath('td[2]/span/text()').re(r'\d+')[0]
			main_page_url = sel.xpath('td[2]/a/@href').extract_first()
			item['main_page_url'] = response.urljoin(main_page_url)

			request = scrapy.Request(item['main_page_url'], callback=self.parse_movie_details)
			request.meta['item'] = item

			# if int(item['ranking']) > self.wanted_num:
			# 	return
			yield request	 

	def parse_movie_details(self, response):
		item = response.meta['item']
		item = self.get_basic_film_info(item, response)
		item = self.get_technical_details(item, response)
		item = self.get_cast_member_info(item, response)
		return item		

	def get_basic_film_info(self, item, response):
		item['director'] = response.xpath('//div/span[@itemprop="director"]/a/span/text()').extract_first()
		item['writers'] = response.xpath('//div/span[@itemprop="creator"]/a/span/text()').extract_first()
		item['sinopsis'] = response.xpath('//div[@itemprop="description"]/text()').extract_first()
		item['genres'] = response.xpath('//div[@itemprop="genre"]/a/text()').extract()
		item['mppa_rating'] = response.xpath('//span[@item="contentRating"]/text()').extract_first()
		return item

	def get_cast_member_info(self, item, response):
		item['cast_members']	= []
		for index, cast_member in enumerate(response.xpath('//div[@id="titleCast"]/table/tr')):
			if index == 0:
				continue

			cast = CastItem()
			cast['ranking'] = index
			cast['actor_name'] = self.get_index(cast_member.xpath('td[2]/a/text()').extract())
			cast['character_name'] = self.get_index(cast_member.xpath('td[4]/div/a/text()').extract())
			item['cast_members'].append(cast)

		return item
		
	def get_technical_details(self, item, response):
		# set default value for the item without values
		for index, details in enumerate(response.xpath('//*[@id="titleDetails"]/div')):
			titleDetails = details.xpath('h4/text()').extract()
			if titleDetails:
				item = self.map_film_details(response, self.get_index(titleDetails), item, index)

		return item		

	def map_film_details(self, response, titleDetails, item, index):

		index += 1

		if titleDetails:
			if 'Language' in titleDetails:
				item['language'] = self.get_index(self.get_title_details(response, index))
			elif 'Country' in titleDetails:
				item['country'] = self.get_index(self.get_title_details(response, index))
			elif 'Budget' in titleDetails:
				item['budget'] = self.get_index(self.get_title_details(response, index))
			elif 'Gross' in titleDetails:
				item['gross_profit'] = self.get_index(self.get_title_details(response, index))
			elif 'Opening Weekend' in titleDetails:
				item['opening_weekend_profit'] = self.get_index(self.get_title_details(response, index))
			elif 'Sound Mix' in titleDetails:
				item['sound_mix'] = self.get_index(self.get_title_details(response, index))
			elif 'Color' in titleDetails:
				item['color'] = self.get_index(self.get_title_details(response, index))
			elif 'Aspect Ratio' in titleDetails:
				item['aspect_ratio'] = self.get_index(self.get_title_details(response, index), 1)
			elif 'Runtime:' in titleDetails:
				item['runtime'] = self.get_index(self.get_title_details(response, index))
		return item

	def get_title_details(self, response, index):
			return response.xpath('//div[@id="titleDetails"]/div['+str(index)+']/a/text()').extract()	

	def get_index(self, item, index=0):
		if item:
			return item[index]
		else:
			return item					

	

