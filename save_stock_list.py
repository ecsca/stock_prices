import pymongo

file = open("./kospi_stock_list.csv", "r")
connection = pymongo.MongoClient("localhost", 10001)
db = connection["stock"]
collection = db["stock_list"]
for line in file:
    splited_line = line.strip().split(",")
    print (splited_line)
    collection.update({"code" : splited_line[1]},
                      { "$setOnInsert" : {"title" : splited_line[2],
                                          "field" : splited_line[3],
                                          "market" : splited_line[0]}},
                      upsert=True)
file.close()
