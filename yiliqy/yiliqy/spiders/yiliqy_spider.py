# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from yiliqy.items import YiliqyItem


#爱奇艺播放数
class YiliqySpider(scrapy.Spider):
    name='yiliqy'
    allowed_domains=["iqiyi.com/"]
    #入口
    def start_requests(self):
        for i in xrange(1,21):
            yield Request("http://so.iqiyi.com/so/q_%E4%BC%8A%E5%88%A9_ctg__t_0_page_"+str(i)+"_p_1_qc_0_rd__site__m_1_bitrate_",
                            callback=self.lists
                          )

    #列表页
    def lists(self, response):
        for l in response.xpath("//ul[@class='mod_result_list']/li[@class='list_item']"):
            url=l.xpath(".//div[@class='result_info result_info-180101']/h3[@class='result_title']/a/@href").extract()
            curl="".join(url)
            key="iqiyi"
            #curl为"" ,报错missing scheme
            #dont_filter 取消allowed_domains设置
            if curl != ""and key in curl:
                    yield Request(
                        curl,
                        callback=self.lists_1,
                        dont_filter=True
                    )

    #详情页
    def lists_1(self, response):

        num= response.xpath("//div[@id='videoArea']/div/@data-player-tvid").extract()
        yield Request(
            "http://mixer.video.iqiyi.com/jp/mixin/videos/" + str(
                num[0]) + "?status=1&callback=window.Q.__callbacks__.",
            callback=self.info,
            dont_filter=True
        )
    #js请求
    def info(self, response):
            item = YiliqyItem()
            item["body"] = response.body
            yield item