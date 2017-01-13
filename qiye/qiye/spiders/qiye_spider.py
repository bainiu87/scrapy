# -*- coding: utf-8 -*-
import scrapy

from scrapy import Request
from qiye.items import QiyeItem

class QiyeSpider(scrapy.Spider):
    name="qiye"
    allowed_domains = ['56ye.net']

    def start_requests(self):
        for i in xrange(1,480):
           yield Request("http://qiye.56ye.net/search.php?areaid=1&page="+str(i),callback=self.parse_list)

    def parse_list(self,response):
        for l in response.xpath("//div[@class='m_l_1 f_l']/div[@class='left_box']/div[@class='list']"):
            url=l.xpath(".//ul/dd[@class='show-info']/li[@class='sup-name']/a[1]/@href").extract()
            yield Request(url[0],callback=self.parse_info)

    def parse_info(self,response):
        for l in response.xpath("//div[@class='body_bg']/div[@class='m'][3]/table/tr"):
            item=QiyeItem()
            item['info']=l.xpath(".//td[@id='side']/div[@class='qy_body']/div[@class='si-wrap']/descendant::text()").extract()
            item['profile']=l.xpath(".//td[@id='main']/div[@class='main_body'][1]/div[@class='lh18 px13 pd10']/descendant::text()").extract()
            item['supply']=l.xpath(".//td[@id='main']/div[@class='main_body'][2]/table/descendant::text()").extract()
            yield item