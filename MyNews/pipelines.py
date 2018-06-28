# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

'''
class MynewsPipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        item["body"] = item["body"].strip()
        item["pubtime"] = item["pubtime"].replace('来源: ','')
        item["pubtime"] = item["pubtime"].strip()
        return item
'''
from MyNews.items import NewsItem
from MyNews.items import ReportItem
from MyNews.items import companybase_personItem
from MyNews.items import companybaseItem

class MynewsPipeline(object):
    def process_item(self, item, spider):
        # 写入json文件
        if isinstance(item, NewsItem):
            print(1)
        elif isinstance(item, ReportItem):
            print(2)
        elif isinstance(item, companybase_personItem):
            print(3)
        elif isinstance(item, companybaseItem):
            print(4)
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item


