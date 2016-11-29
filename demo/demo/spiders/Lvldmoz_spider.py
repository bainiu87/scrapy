import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import Request
from demo.items import LvlItem
from scrapy.contrib.linkextractors import LinkExtractor
class LvlitemSpider(scrapy.Spider):
    name="lvl"
    allowed_domains = ["ll.gov.cn"]
    start_urls=[
        "http://www.ll.gov.cn/lvliang/"
    ]
    def parse(self, response):
        item = LvlItem()
        for sel in response.xpath('//ul[@class="e2"]'):
                item['uu']=response.url
                item['title']=sel.xpath(".//li/a/text()").extract()
                item['link']=sel.xpath(".//li/a@href").extract()
                yield item
        nextlin=response.xpath("//ul[@class='pagelist']/li/a/@href").extract()
        if nextlin:
            for i in xrange(1,10):
                yield Request(response.urljoin(nextlin[i]),callback=self.parse)



