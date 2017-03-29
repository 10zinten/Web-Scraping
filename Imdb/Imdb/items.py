# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MovieItem(Item):
    title = Field()
    rating = Field()
    ranking = Field()
    release_year = Field()
    main_page_url = Field()

    # Some more details
    director = Field()
    writers = Field()
    runtime = Field()
    sinopsis = Field()
    genres = Field()
    mppa_rating = Field()
    budget = Field()
    language = Field()
    country = Field()

    #some technical details
    gross_profit = Field()
    opening_weekend_profit = Field()
    aspect_ratio = Field()
    sound_mix = Field()
    color = Field()

    cast_members = Field()

    # cast_member's details
class CastItem(Item):
	actor_name = Field()
	character_name = Field()
	ranking = Field()