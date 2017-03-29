# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ConifersItem(scrapy.Item):
    name = scrapy.Field()
    genus = scrapy.Field()
    species = scrapy.Field()
    pass 
