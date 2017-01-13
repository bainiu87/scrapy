# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YilitbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sell =scrapy.Field()
    eva = scrapy.Field()
    storename=scrapy.Field()
