#-*- coding: utf-8 -*-

import scrapy
import pymongo
from stock.items import StockItem

class stockSpider(scrapy.Spider):
    name = "stock"
    allowed_domains = ["naver.com"]
    base_url = "http://finance.naver.com/item/sise_day.nhn?code="

    def start_requests(self):
        collection = pymongo.MongoClient("localhost", 10001)["stock"]["stock_list"]
        for obj in collection.find():
            yield scrapy.Request(self.base_url + obj["code"], self.parse)

    def parse(self, response):
        last_index = int(response.xpath('//td/a/@href').extract()[-1].split("=")[-1])
        code = response.xpath('//td/a/@href').extract()[0].split("=")[-2].split("&")[0]
        url = self.base_url + code
        #TODO : if total page number is under 11?(no last_index)
        #TODO : Can we use url join?
        #TODO : Can we parse only first page if db has old data?
        print url
        collection = pymongo.MongoClient("localhost", 10001)["stock"]["stock_price"]
        if (collection.find({"code" : code}).count() > 0):
            yield scrapy.Request(url + "&page=1", callback=self.parse_page)
        else:
            for i in range(1, last_index + 1) :
                yield scrapy.Request(url + "&page=" + str(i), callback=self.parse_page)

    def parse_page(self, response):
        for sel in response.xpath('//tr') :
            code = response.xpath('//td/a/@href').extract()[0].split("=")[-2].split("&")[0]
            l = sel.xpath('td/span/text()').extract()
            if (not l):
                continue
            item = StockItem()
            item['code'] = code
            item['date'] = l[0]
            item['final_price']= l[1].replace(",", "")
            item['highest_price'] = l[4].replace(",", "")
            item['lowest_price']= l[5].replace(",", "")
            item['trading_volume'] = l[6].replace(",", "")
            yield item
