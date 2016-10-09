# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import pymongo
import settings
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

class StockPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        self.collection.update({"code" : item['code'].encode('utf-8'), "date" : item['date'].encode('utf-8')},
                               { "$setOnInsert": {"final_price" : item["final_price"].encode("utf-8"),
                                                  "highest_price" : item["highest_price"].encode("utf-8"),
                                                  "lowest_price" : item["lowest_price"].encode("utf-8"),
                                                  "trading_volume" : item["trading_volume"].encode("utf-8")}},
                               upsert=True)
        return item
