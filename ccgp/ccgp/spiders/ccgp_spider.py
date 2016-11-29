import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from ccgp.items import CcgpItem

class CcgpSpider(CrawlSpider):
    name="ccgp"
    allowed_domains=['ccgp.gov.cn']

    rules = [Rule(LinkExtractor(allow='/20\d+/t\d+_\d+\.htm'), callback='parse_info')]
    def start_requests(self):
        yield Request("http://www.ccgp.gov.cn/cggg/zygg/zbgg/index.htm")
        for i in xrange(1,26):
            yield Request("http://www.ccgp.gov.cn/cggg/zygg/zbgg/index_"+str(i)+".htm")
    def parse_info(self, response):
        for l in response.xpath("//div[@class='vT_detail_main']"):
            item=CcgpItem()
            item['profile']=l.xpath(".//div[@class='table']/table/descendant::text()").extract()
            item['detail']=l.xpath(".//div[@class='vT_detail_content w760c']/descendant::text()").extract()
            yield item




