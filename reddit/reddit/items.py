# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class RedditItem(Item):
    title = Field()
    url = Field()
    images = Field()
    image_urls = Field()

