#-*- coding: utf-8 -*-

import scrapy
from stock.items import StockItem

class stockSpider(scrapy.Spider):
    name = "stock"
    allowed_domains = ["naver.com"]
    start_urls = [
            "http://finance.naver.com/item/sise_day.nhn?code=002900"
            ]

    def parse(self, response):
        last_index = int(response.xpath('//td/a/@href').extract()[-1].split("=")[-1])
        url = "http://finance.naver.com/item/sise_day.nhn?code=002900"
        for i in range(1, last_index + 1) :
            yield scrapy.Request(url + "&page=" + str(i), callback=self.parse_page)

    def parse_page(self, response):
        for sel in response.xpath('//tr') :
            l = sel.xpath('td/span/text()').extract()
            if (not l):
                continue
            item = StockItem()
            item['code'] = '002900'
            item['date'] = l[0]
            item['final_price']= l[1]
            item['highest_price'] = l[4]
            item['lowest_price']= l[5]
            item['trading_volume'] = l[6]
            yield item
