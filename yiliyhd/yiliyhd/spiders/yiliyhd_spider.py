# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from lxml import etree
from yiliyhd.items import YiliyhdItem
#抓取一号店伊利评价数
class YiliyhdSpider(scrapy.Spider):
    name="yiliyhd"

    def start_requests(self):
        for l in xrange(1,13):
            for i in xrange(1,3):
                if i == 1:
                    yield Request(
                        "http://search.yhd.com/c0-0-0/b-9138/a-s1-v4-p"+str(l)+"-price-d0-f0-m1-rt1-pid-mid0-k%E4%BC%8A%E5%88%A9/#page="+str(l)+"&sort=1",
                        callback=self.lists_1
                    )
                if i == 2:
                    yield Request(
                        "http://search.yhd.com/searchPage/c0-0-0/b-9138/a-s1-v4-p"+str(l)+"-price-d0-f0-m1-rt1-pid-mid0-k%E4%BC%8A%E5%88%A9/?callback=&isGetMoreProducts=1&moreProductsDefaultTemplate=0&isLargeImg=0&moreProductsFashionCateType=2&nextAdIndex=0&nextImageAdIndex=0&adProductIdListStr=&fashionCateType=2&firstPgAdSize=0&_=",
                        callback=self.lists_2
                    )
    def lists_1(self,response):
        for l in response.xpath("//div[@class='mod_search_pro']"):
            item = YiliyhdItem()
            item['num'] = l.xpath(".//div[@class='itemBox']/p[@class='proPrice'][2]/span[@class='comment']/a/text()").extract()
            item['name'] = l.xpath(".//div[@class='itemBox']/p[@class='proName clearfix']/a[1]/text()").extract()
            item['storename'] = l.xpath(".//div[@class='itemBox']/p[@class='storeName ']/a/text()").extract()
            yield item
    def lists_2(self,response):
        #将json数据包处理为dice，转码为utf8
        #将html字符串处理为html对象，使用xpath查找
        text=json.loads(response.body)['value'].encode('utf8')
        re=etree.HTML(text)
        for l in re.xpath("//div[@class='mod_search_pro']"):
            item=YiliyhdItem()
            item['num']=l.xpath(".//div[@class='itemBox']/p[@class='proPrice'][2]/span[@class='comment']/a/text()")
            item['name']=l.xpath(".//div[@class='itemBox']/p[@class='proName clearfix']/a[1]/text()")
            item['storename']=l.xpath(".//div[@class='itemBox']/p[@class='storeName ']/a/text()")
            yield item

