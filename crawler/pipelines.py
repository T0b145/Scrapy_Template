# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from datetime import datetime
#import pymongo # activate if you want to use the pipeline
#import dataset # activate if you want to use the pipeline

from itemadapter import ItemAdapter

class JsonWriterPipeline:

    def open_spider(self, spider):
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y%m%d%H%M%S")
        self.file = open('./crawls/{}items.jl'.format(timestampStr), 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class MongoPipeline(object):
    def __init__(self, uri, db, collection_name):
        self.uri = uri
        self.db = db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('DB_URI'),
            db=crawler.settings.get('DB_DATABASE', 'items'),
            collection_name=crawler.settings.get('DB_TABLE_NAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[self.db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item


class MySQLPipeline(object):
    def __init__(self, uri, db, user, password, table_name):
        self.uri = uri
        self.db = db
        self.user = user
        self.password = password
        self.table_name = table_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('DB_URI'),
            db=crawler.settings.get('DB_DATABASE'),
            user=crawler.settings.get('DB_USER'),
            password=crawler.settings.get('DB_PASSWORD'),
            table_name = crawler.settings.get('DB_TABLE_NAME')
        )

    def open_spider(self, spider):
        self.db = dataset.connect('postgresql://{}:{}@{}:5432/{}'.format(self.user,self.password,self.uri,self.db))
        self.table = self.db[self.table_name]

    def close_spider(self, spider):
        print ("Spider Closed")

    def process_item(self, item, spider):
        #self.table.insert({"test":"test"})
        self.table.insert(dict(item))
        return item
