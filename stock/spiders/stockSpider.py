#-*- coding: utf-8 -*-

import scrapy

class stockSpider(scrapy.Spider):
    name = "stock"
    allowed_domains = ["naver.com"]
    start_urls = [
            "http://finance.naver.com/item/sise_day.nhn?code=002900&page=1"
            ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            for sel in response.xpath('//tr') :
                l = sel.xpath('td/span/text()').extract()
                if (not l):
                    continue
                for i in l:
                    date = l[0]
                    final_price = l[1]
                    highest_price = l[4]
                    lowest_price = l[5]
                    trading_volume = l[6]
                print date, final_price, highest_price, lowest_price, trading_volume
