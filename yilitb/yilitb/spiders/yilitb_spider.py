# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from yilitb.items import YilitbItem
from urlparse import urljoin

#淘宝网 伊利店名， 销售量  评价数
#需要splash
class YilitbSpider(scrapy.Spider):

    name = 'yilitb'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        #'Referer': 'https: // www.taobao.com /',
        'Upgrade - Insecure - Requests': 1,
        #'User - Agent': 'Mozilla / 5.0(WindowsNT6.1;WOW64;rv:50.0) Gecko / 20100101Firefox / 50.0'
    }

    def start_requests(self):
        a=-44
        for l in xrange(1,101):
            a+=44
            uu="https://s.taobao.com/search?q=%E4%BC%8A%E5%88%A9&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170111&bcoffset=&ntoffset=&p4ppushleft=1%2C48&s="+str(a)
            #meta 中的url参数为需要爬取的地址，参考splash API文档
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
            #请求地址为splash 地址
            yield Request(
                #"http://192.168.99.100:8050/",
                "http://192.168.1.194:8050/",
                headers=self.headers,
                meta=meta,
                callback=self.lists
            )
    def lists(self,response):

        print '----------------'+response.url
        for l in response.xpath("//div[@class='item J_MouserOnverReq item-ad  '] | //div[@class='item J_MouserOnverReq  ']"):
            uu=l.xpath(".//div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']/div[@class='row row-2 title']/a/@href").extract()
            if 'taobao' in uu[0]:
                item = YilitbItem()
                item['storename'] = l.xpath(".//div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']/div[@class='row row-3 g-clearfix']/div[@class='shop']/a/span[2]/text()").extract()
                url = urljoin('https:',uu[0]).encode('utf8')
                print url
                yield Request(
                    "http://192.168.1.194:8050/render.html?url="+url+"&wait=5&images=0&render_all=1",
                    headers=self.headers,
                    meta={'item':item},
                    callback=self.info,
                )
    def info(self,response):
        item=response.meta['item']
        #item=YilitbItem()
        #item['storename']=response.xpath("//div[@class='shop-name-wrap']/a/text()").extract()
        item['eva']=response.xpath("//li[@id='J_Counter']/div[@class='tb-counter-bd']/div[@class='tb-rate-counter']/a/strong/text()").extract()
        item['sell'] =response.xpath("//li[@id='J_Counter']/div[@class='tb-counter-bd']/div[@class='tb-sell-counter']/a/strong/text()").extract()
        yield item