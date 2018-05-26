# -*- coding: utf-8 -*-


import json
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from scrapy_splash import SplashRequest
from scrapy_redis.spiders import RedisSpider
from ..items import ReportItem
from scrapy import Request
from ..headers import Eastmoneyheaders
import requests
import base64
from lxml import etree

class EastmoneyReportSpider(RedisSpider):
    """Spider that reads urls from redis queue (qqnews:start_urls)."""


    start_urls = ["http://data.eastmoney.com/report/#dHA9MCZjZz0wJmR0PTImcGFnZT0x"]
    #start_urls = ["http://www.eastmoney.com"]

    name = 'EastmoneyReport'
    redis_key = 'EastmoneyReport:start_urls'
    taglist = ['ent','sports','finance','tech','report']

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('eastmoney.com', 'data.eastmoney.com')
        #self.allowed_domains = filter(None, domain.split(','))
        super(EastmoneyReportSpider, self).__init__(*args, **kwargs)
    # request需要封装成SplashRequest
    def parse(self,response):
        #print(response)
        for url in self.start_urls:
            yield SplashRequest(url
                                , self.parse_next
                                , args={'wait': '1.5'}
                                ,headers=Eastmoneyheaders
                                ,dont_filter=True
                                # ,endpoint='render.json'
                                )
    def parse_next(self,response):
        # 取得总页数
        print(response)
        html = etree.HTML(response.text)
        vlist = html.xpath("//div[@id='PageCont']//a/text()")
        page_total = int(vlist[-3])
        #page_total = 3
        # 循环遍历所有页
        for i in range(1,page_total):
        #for i in range(20,25):
            # 得到每页的url
            url_param='tp=0&cg=0&dt=2&page='+str(i)
            encodestr = base64.b64encode(url_param.encode('utf-8'))
            url_encodestr=str(encodestr, 'utf-8')
            #url = 'http://stock.eastmoney.com/news/cgszb_'+str(i)+'.html'
            url = 'http://data.eastmoney.com/report/#'+url_encodestr
            print('URL的值为:',url)
            #yield Request(url,callback=self.parsepage,dont_filter=True)
            yield SplashRequest(url
                                , self.parsepage
                                , args={'wait': '1.5'}
                                ,headers=Eastmoneyheaders
                                ,dont_filter=True
                                #,endpoint='render.html'
                                )

    def parsepage(self,vresponse):
        #print(vresponse)
        # 得到新闻详情页的url列表
        post_url_list = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[6]/div[@class='report_tit']/a/@href").extract()
        pubdate = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[2]/span[@class='txt']/@title").extract()
        stkcode = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[3]/a/text()").extract()
        stkname = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[4]/a/text()").extract()
        reportname = vresponse.xpath("//table[@id='dt_1']/tbody/tr/td[6]/div[@class='report_tit']/a/text()").extract()
        ywpj = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[7]/text()").extract()
        #评级变动
        pjbd = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[8]/text()").extract()
        #评级机构
        pjjg = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[9]/a/text()").extract()
        #预测收益1
        ycsy1 = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[10]/text()").extract()
        #市盈率1
        ycsyl1 = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[11]/text()").extract()
        #预测收益2
        ycsy2 = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[12]/text()").extract()
        #市盈率2
        ycsyl2 = vresponse.xpath("//div[@class='content tb14']/table[@id='dt_1']/tbody/tr/td[13]/text()").extract()

        # 遍历所有新闻url
        for i,post_url in enumerate(post_url_list):
            metavalue={'tag':'report',
                       'pubdate':pubdate[i],
                       'stkcode':stkcode[i],
                       'stkname':stkname[i],
                       'reportname':reportname[i],
                       'ywpj':ywpj[i],
                       'pjbd':pjbd[i],
                       'pjjg':pjjg[i],
                       'ycsy1':ycsy1[i],
                       'ycsyl1':ycsyl1[i],
                       'ycsy2':ycsy2[i],
                       'ycsyl2':ycsyl2[i]
                       }
            post_url='http://data.eastmoney.com/'+post_url
            yield Request(post_url, callback=self.parsebody, headers=Eastmoneyheaders,meta=metavalue,dont_filter=True)

    # 抽取页面数据
    def parsebody(self,response):
        meta = response.meta

        item = ReportItem()
        item['tag'] = meta['tag']
        item['pubdate'] = meta['pubdate']
        item['pubtime'] = response.xpath("//div[@class='report-infos']/span[2]/text()").extract()[0]
        item['refer'] = '东方财富'
        item['stkcode'] = meta['stkcode']
        item['stkname'] = meta['stkname']
        item['reportname'] = meta['reportname']

        #item['body'] =response.xpath("//div[@id='ContentBody']/div[@class='newsContent']").xpath('string(.)').extract().strip()
        item['body'] =str(response.xpath("//div[@id='ContentBody']/div[@class='newsContent']").extract()).strip().replace('\\r\\n','')
        item['url'] = response.url
        item['ywpj'] = meta['ywpj']
        item['pjbd'] = meta['pjbd']
        item['pjjg'] = meta['pjjg']
        item['ycsy1'] = meta['ycsy1']
        item['ycsyl1'] = meta['ycsyl1']
        item['ycsy2'] = meta['ycsy2']
        item['ycsyl2']=meta['ycsyl2']
        yield item