# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import scrapy_splash
import scrapyjs
from yilitm.items import YilitmItem

#天猫销售量，评价数，商店名
#需要使用splash,无头浏览器，所以需要设置头部，同时加载useragent池，设置cookie开启，模拟真正浏览器，防止被ban
#splash 可以参考http://ae.yyuap.com/pages/viewpage.action?pageId=919763
#在设置中需要加入DUPEFILTER_DEBUG=True ，可以在log中看到splash中的详细加载情况
#splash 需要使用docker
#需要加入dont_filter ,否则会报错：Filtered duplicate request（过滤重复请求）
class YilitmSpider(scrapy.Spider):
    name='yilitm'

    def start_requests(self):
        #wait为splash浏览器等待响应时间，所以在设置DOWNLOAD_DELAY时，应该比该响应时间小一点

         a=0
         for l in xrange(1,31):
             if l == 1:
                 meta = {
                     'splash': {
                         'endpoint': 'render.html',
                         'args': {
                             'url':"https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.P2AYuF&brand=20328&q=%D2%C1%C0%FB&sort=s&style=g&from=mallfp..pc_1_suggest&suggest=0_1&active=2&smAreaId=110100&type=pc",
                             'wait': 5,
                             'images': 0,
                             'render_all': 1
                         }

                     }
                 }
                 yield Request(
                                "http://192.168.99.100:8050/",
                                meta=meta,
                                callback=self.lists
                                  )
             if l != 1:
                 a+=60
                 uu="https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0&brand=20328&s="+str(a)+"&q=%D2%C1%C0%FB&sort=s&style=g&from=mallfp..pc_1_suggest&suggest=0_1&active=2&smAreaId=110100&type=pc#J_Filter"
                 meta = {
                     'splash': {
                         'endpoint': 'render.html',
                         'args': {
                             'url': uu,
                             'wait': 5,
                             'images': 0,
                             'render_all': 1
                         }

                     }
                 }
                 yield Request(
                                "http://192.168.99.100:8050/",
                                 meta=meta,
                                 callback=self.lists
                                  )

    def lists(self, response):
        for l in response.xpath("//div[@id='J_ItemList']/div[@class='product  ']"):
            item=YilitmItem()
            item['name']=l.xpath(".//div[@class='product-iWrap']/div[@class='productShop']/a/descendant::text()").extract()
            item['sell_num']=l.xpath(".//div[@class='product-iWrap']/p[@class='productStatus']/span[1]/em/text()").extract()
            item['eva_num']=l.xpath(".//div[@class='product-iWrap']/p[@class='productStatus']/span[2]/a/text()").extract()
            yield item
