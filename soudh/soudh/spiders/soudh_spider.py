# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request
from urlparse import urljoin
from soudh.items import SoudhItem
class SoudhSpider(Spider):
    name='soudh'
    allowed_domains=['soudh.com']
    def start_requests(self):
        for l in xrange (1,587):
            yield Request("http://www.soudh.com/province-1-"+str(l)+".html",callback=self.parse_list)
    def parse_list(self,response):
        for i in response.xpath("//div[@class='leftbox comlist']/ul/li"):
            url=i.xpath(".//a/@href").extract()
            urll=urljoin("http://www.soudh.com/",url[0])
            yield Request(urll,callback=self.parse_info)
    def parse_info(self,response):
        for l in response.xpath("//div[@id='main']/div[@id='left']"):
            item = SoudhItem()
            item["phone"] = l.xpath(".//div[@class='leftbox'][2]/descendant::text()").extract()
            tel=l.xpath("//div[@id='main']/div[@id='left']/div[@class='leftbox'][2]/div[@id='content']/table/tr/td[1]/li[3]/img/@src").extract()
            telphone=l.xpath("//div[@id='main']/div[@id='left']/div[@class='leftbox'][2]/div[@id='content']/table/tr/td[1]/li[4]/img/@src").extract()
            item["image_urls"] =[urljoin("http://www.soudh.com/",tel[0]),urljoin("http://www.soudh.com/",telphone[0])]
            item["profile"] = l.xpath(".//div[@class='leftbox'][3]/descendant::text()").extract()
            item["abstract"] = l.xpath(".//div[@class='leftbox'][4]/descendant::text()").extract()
            yield item

