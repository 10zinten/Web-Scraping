# -*- coding: utf-8 -*-
import scrapy


class SubredditSpider(scrapy.Spider):
    name = "subreddit"
    allowed_domains = ["reddit.com"]
    start_urls = ['http://reddit.com/r/python']

    def parse(self, response):
        for submission_sel in response.css("a.title"):
            item = {}
            item["url"] = submission_sel.css("::attr(href)").extract_first()
            item["title"] = submission_sel.css("::text").extract_first()
            yield item
