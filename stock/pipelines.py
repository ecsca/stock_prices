# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

class StockPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('host', 'id', 'pasword', 'dbname')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        print int(item['code']), item['date'], int(item['final_price']), int(item['highest_price']), int(item['lowest_price'])
        try:
            #can we get better db schema?
            self.cursor.execute("""INSERT INTO stock_prices
            (code, date, final_price, highest_price, lowest_price, trading_volume)
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                           (item['code'].encode('utf-8'),
                            item['date'].encode('utf-8'),
                            item['final_price'].encode('utf-8'),
                            item['highest_price'].encode('utf-8'),
                            item['lowest_price'].encode('utf-8'),
                            item['trading_volume'].encode('utf-8')))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item
