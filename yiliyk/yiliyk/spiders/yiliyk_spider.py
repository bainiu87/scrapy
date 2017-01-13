# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from yiliyk.items import YiliykItem

#优酷播放数
class YiliykuSpider(scrapy.Spider):
    name="yiliyk"
    allowed_domains=["soku"]
    #入口
    def start_requests(self):
        for i in xrange(1,99):
            if i == 1:
                for l in xrange(0,3):
                    if l == 0:
                        yield Request("http://www.soku.com/search_video/q_%E4%BC%8A%E5%88%A9_orderby_1_limitdate_0?site=14&page=1&spm=a2h0k.8191407.0.0",
                                      callback=self.list_1
                                      )
                    if l == 1:
                        yield Request(
                            "http://www.soku.com/search_video_ajax/q_%E4%BC%8A%E5%88%A9_orderby_1_limitdate_0?site=14&page=2",
                            callback=self.list_2
                            )
                    if l == 2:
                        yield Request(
                            "http://www.soku.com/search_video_ajax/q_%E4%BC%8A%E5%88%A9_orderby_1_limitdate_0?site=14&page=3",
                            callback=self.list_2
                        )
            else:
                yield Request("http://www.soku.com/search_video/q_%E4%BC%8A%E5%88%A9_orderby_1_limitdate_0?site=14&page="+str(i)+"&spm=a2h0k.8191407.0.0",
                              callback=self.list_1
                              )
    def list_1(self, response):
        for l in response.xpath("//div[@class='sk-vlist clearfix']/div[@class='v']"):
            item=YiliykItem()
            item["name"]=l.xpath(".//div[@class='v-meta va']/div[@class='v-meta-title']/a/descendant::text()").extract()
            item["url"]=l.xpath(".//div[@class='v-meta va']/div[@class='v-meta-title']/a/@href").extract()
            item["num"]=l.xpath(".//div[@class='v-meta va']/div[@class='v-meta-entry']/div[@class='v-meta-data'][2]/span[@class='pub']/text()").extract()
            yield item
    def list_2(self, response):
        for l in response.xpath("//div[@class='v']"):
            item = YiliykItem()
            item["name"] = l.xpath(".//div[@class='v-meta va']/div[@class='v-meta-title']/a/descendant::text()").extract()
            item["url"] = l.xpath(".//div[@class='v-meta va']/div[@class='v-meta-title']/a/@href").extract()
            item["num"] = l.xpath(".//div[@class='v-meta va']/div[@class='v-meta-entry']/div[@class='v-meta-data'][2]/span[@class='pub']/text()").extract()
            yield item