# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    date = scrapy.Field()
    final_price = scrapy.Field()
    highest_price = scrapy.Field()
    lowest_price = scrapy.Field()
    trading_volume = scrapy.Field()
    pass
