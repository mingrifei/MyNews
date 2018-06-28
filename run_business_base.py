# -*- coding: utf-8 -*-
from scrapy import cmdline
import redis


r = redis.Redis(host='127.0.0.1',port=6379,db=14)
r.lpush('BusinessBaseInfo:start_urls','http://120.77.35.204:8888/')
cmdline.execute("scrapy crawl BusinessBaseInfo".split())
