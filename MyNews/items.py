# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join



class NewsItem(Item):
    # define the fields for your item here like:
    title = Field() #标题
    body = Field() #内容
    url = Field()
    refer = Field()
    tag = Field()
    pubtime = Field() #发布时间
    crawled = Field()
    spider = Field()

class ReportItem(Item):
    # define the fields for your item here like:
    tag = Field()
    pubdate = Field()
    pubtime = Field()
    refer = Field()
    stkcode = Field()
    stkname = Field()
    reportname = Field()
    body = Field()
    url = Field()
    ywpj = Field()
    pjbd = Field()
    pjjg = Field()
    ycsy1 = Field()
    ycsyl1 = Field()
    ycsy2 = Field()
    ycsyl2 = Field()
    crawled = Field()
    spider = Field()

class companybaseItem(Item):
    # define the fields for your item here like:
    stkcode = Field()
    stkname = Field()
    companyname = Field()
    companyaddress= Field()
    companypostcode = Field()
    firstregaddress = Field()
    regcode = Field()
    legalname = Field()
    ceoname = Field()
    url = Field()
    crawled = Field()
    spider = Field()
    body = Field()
class companybase_personItem(Item):
    # define the fields for your item here like:
    stkcode = Field()
    stkname = Field()
    personname = Field()
    personjob= Field()
    personbirth = Field()
    personsex = Field()
    personedu = Field()
    url = Field()
    crawled = Field()
    spider = Field()
    body = Field()


class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()


class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
