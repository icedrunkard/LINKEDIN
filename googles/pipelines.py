# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import pymongo
#from googles.settings import COLLECTION_NAME


class MongoNewPipeline(object):
    #collection_name = COLLECTION_NAME+'_studentsLinka'

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_HOST'),#localhost
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        
        self.db=self.client[item['short']]
        self.collection_name=item['dpt']+'_studentsProfile'
        self.db[self.collection_name].update({'name_code': item['name_code']}, dict(item), True)
        #self.db[self.collection_name].insert( dict(item))
        return item

