# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from yilijd.items import YilijdItem

#京东评论数
class YilijdSpider(scrapy.Spider):
    name = "yilijd"
    allowed_domains=["search.jd"]

    #请求入口
    def start_requests(self):
       p=1
       s=1
       for i in xrange(1,71):
           if i == 1:
               for l in xrange(0,2):
                   if l == 0:
                       yield Request(
                           "https://search.jd.com/Search?keyword=%E4%BC%8A%E5%88%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&psort=3&ev=exbrand_%E4%BC%8A%E5%88%A9%40&page="+str(p)+"&s="+str(s)+"&click=0",
                            callback=self.list_1)
                   if l ==1:
                        yield Request(
                            "https://search.jd.com/s_new.php?keyword=%E4%BC%8A%E5%88%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&psort=3&ev=exbrand_%E4%BC%8A%E5%88%A9%40&page=2&s=31&scrolling=y&pos=30&tpl=1_M",
                            callback=self.list_2)

           else:
                p+=2
                s+=60
                for l in xrange (0,2):
                    if l == 0:
                        yield Request(
                            "https://search.jd.com/Search?keyword=%E4%BC%8A%E5%88%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&psort=3&ev=exbrand_%E4%BC%8A%E5%88%A9%40&page="+str(p)+"&s="+str(s)+"&click=0",
                            callback=self.list_1)
                    if l == 1:
                        yield Request(
                            "https://search.jd.com/s_new.php?keyword=%E4%BC%8A%E5%88%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&psort=3&ev=exbrand_%E4%BC%8A%E5%88%A9%40&page="+str(p+1)+"&s="+str(s+30)+"&scrolling=y&pos=30&log_id=1482743188.82235&tpl=1_M",
                            callback=self.list_2)
    #获取静态页面
    def list_1(self,response):
        for l in response.xpath("//div[@id='J_goodsList']/ul[@class='gl-warp clearfix']/li"):
            item = YilijdItem()
            item["num"]=l.xpath(".//div[@class='gl-i-wrap']/div[@class='p-commit']/strong/a/descendant::text()").extract()
            yield item

    #获取JS页面
    def list_2(self,response):
        for l in response.xpath("//li"):
            item = YilijdItem()
            item["num"]=l.xpath(".//div[@class='gl-i-wrap']/div[@class='p-commit']/strong/a/descendant::text()").extract()
            yield item