# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Site(scrapy.Item):
  domain = scrapy.Field()
  redirect_domains = scrapy.Field()
  title = scrapy.Field()
  description = scrapy.Field()
  html = scrapy.Field()
  outlink_domains = scrapy.Field()
  last_updated = scrapy.Field()
