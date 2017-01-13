# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from yilitx.items import YilitxItem

#腾讯视频播放量
class YilitxSpider(scrapy.Spider):
    name='yilitx'
    #入口
    def start_requests(self):
        for l in xrange(1,21):
            yield Request("https://v.qq.com/x/search/?ses=qid%3DYr8L8rDMQgeMaKtjcUH06_oDFx2b-UR4Djwlv7oDEjMlBGymhhrBQQ%26last_query%3D%E4%BC%8A%E5%88%A9%26tabid_list%3D0%7C2%7C1%7C3%7C4%7C11%7C6%7C12%7C14%7C5%7C17%7C8%7C13%7C9%7C15%7C20%7C7%26tabname_list%3D%E5%85%A8%E9%83%A8%7C%E7%94%B5%E8%A7%86%E5%89%A7%7C%E7%94%B5%E5%BD%B1%7C%E7%BB%BC%E8%89%BA%7C%E5%8A%A8%E6%BC%AB%7C%E6%96%B0%E9%97%BB%7C%E7%BA%AA%E5%BD%95%E7%89%87%7C%E5%A8%B1%E4%B9%90%7C%E4%BD%93%E8%82%B2%7C%E9%9F%B3%E4%B9%90%7C%E6%B8%B8%E6%88%8F%7C%E5%8E%9F%E5%88%9B%7C%E8%B4%A2%E7%BB%8F%7C%E7%83%AD%E4%BA%AB%7C%E6%95%99%E8%82%B2%7C%E6%AF%8D%E5%A9%B4%7C%E5%85%B6%E4%BB%96&q=%E4%BC%8A%E5%88%A9&stag=3&cur="+str(l)+"&cxt=tabid%3D0%26sort%3D0%26pubfilter%3D0%26duration%3D0%26cluster_list%3Dseriesxxhcaoz1st%2Bseriesxxhcaoz1st",
                      callback=self.lists
                      )
    #列表页
    def lists(self,response):
        for l in response.xpath("//div[@class='wrapper']/div[@class='wrapper_main']/div[@class='result_item result_item_h']"):
            url=l.xpath(".//h2[@class='result_title']/a/@href").extract()
            curl="".join(url)
            key="qq"
            if curl!="" and key in curl:
                yield Request(
                    curl,
                    callback=self.info
                )
    #爬取播放量、标题
    def info(self, response):
        item=YilitxItem()
        item['num']=response.xpath("//div[@class='action_item action_count']/a/span[@class='icon_text']/em[@id='mod_cover_playnum']/text()").extract()
        item['name']=response.xpath("//div[@class='video_base video_base_collect']/h1[@class='video_title']/text()").extract()
        yield item