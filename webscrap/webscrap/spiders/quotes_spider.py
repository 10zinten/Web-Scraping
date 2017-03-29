import scrapy 

class QuotesSpider(scrapy.Spider):
	"""
	This is Spider class which uses to scrap infomation from a website.
	It must be subclass of scrapy.Spider and define the initial requests to make.
	"""
	#Identifies the spiders
	name = "quotes" 

	# default Emplementation of start_request() to create the initial 
	# request for the Spider.
	start_urls = [ 
		'http://quotes.toscrape.com/page/1',
	 	'http://quotes.toscrape.com/page/2', 
	]
	
	# def start_requests(self):
	# 	"""
	# 	- It Returns an iterable of Requests which the spider will begin to crawl from.
	# 	- Return can be a list of requests or write a generator functioin.
	# 	"""
	# 	urls = [
	# 		'http://quotes.toscrape.com/page/1',
	# 		'http://quotes.toscrape.com/page/2', 
	# 	]
	# 	for url in urls:
	# 		yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		"""
		- Handle the response downloaded for each of the requests made.
		- It usually parses the response, extracting the scraped data as dicts
		  and also finding new URL to follow and creating new request from them.
		- The response parameter is an instance of TextResponse that holds the page
		  content and futher helpful methods to handle it.
		- It is Scrapy's default callback method so no to call explicity when start_requests 
		  not implemented, but start_url.    
		""" 
		# page = response.url.split("/")[-2]
		# filename = 'quotes-%s.html' % page
		# with open(filename, 'wb') as f:
		# 	f.write(response.body)
		# self.log('Saved file %s' % filename)
		
		for quote in response.css('div.quote'):
			yield {
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('small.author::text').extract_first(),
				'tags': quote.css('div.tags a.tag::text').extract(),
			}

		next_page = response.css('li.next a::attr(href)').extract_first()
		if next_page:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)	