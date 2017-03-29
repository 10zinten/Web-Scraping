# -*- coding: utf-8 -*-
import random
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from reddit.items import RedditItem


class Reddit2Spider(CrawlSpider):
    name = "pic"
    allowed_domains = ["www.reddit.com"]
    start_urls = ['http://www.reddit.com/r/pics/']

    rules = [
    	Rule(LinkExtractor(
    		allow=['r/pics/\?count=\d*&after=\w*']),
    		callback='parse_item',
    		follow=True)
    ]

    # my_property = "file-name" # static property

    # @property 
    # def my_property(self):    # dynamic property
    # 	return random.randint(0, 100)


    def parse_item(self, response):
        sel_list = response.css('div.thing')

        for sel in sel_list:
        	item = RedditItem()
        	item['title'] = sel.xpath('div/p/a/text()').extract()
        	item['url'] = sel.xpath('a/@href').extract()
        	item['image_urls'] = sel.xpath('a/@href').extract()
         	yield item
