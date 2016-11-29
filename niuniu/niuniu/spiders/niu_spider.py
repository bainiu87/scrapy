import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from niuniu.items import NiuniuItem

class NiuniuSpaider(Spider):
    name='niuniu'
    allowed_domains=['mininova.org/']
    start_urls=['http://www.mininova.org/']
    rules=[Rule(LinkExtractor(allow=['/tor/\d+']),'parse_all')]
    def parse_all(self,response):
        item=NiuniuItem()
        item['url'] = response.url
        item['name'] = response.xpath("//h1/text()").extract()
        item['description'] = response.xpath("//div[@id='description']").extract()
        item['size'] = response.xpath("//div[@id='specifications']/p[2]/text()[2]").extract()
        return item

