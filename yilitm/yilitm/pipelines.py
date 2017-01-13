# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import re

class YilitmPipeline(object):
    def __init__(self):
        self.connsql = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='scrapy',charset='utf8')
        self.cur = self.connsql.cursor()
    def process_item(self, item, spider):
        text=dict(item)
        #key为万的accie编码
        key=u'\u4e07'

        #评论量
        if  key in text['eva_num'][0]:
            #正则提取数字
            b=re.findall("\d+\.?\d*",text['eva_num'][0])
            eva_num=str(int(float(b[0])*10000))
        else:
            eva_num=str(text['eva_num'][0])

        #月销售量
        if key in text['sell_num'][0]:
            s=re.findall("\d+\.?\d*",text['sell_num'][0])
            sell_num=str(int(float(s[0])*10000))
        else:
            s=re.findall("\d+\.?\d*",text['sell_num'][0])
            sell_num=str(s[0])

        #店铺名称
        name=''.join(text['name']).encode('utf8')

        #存入数据库
        sql = "insert into yilitm (eva,name,sell)value('"+eva_num+"','"+name+"','"+sell_num+"')"
        self.cur.execute(sql)
        self.connsql.commit()
        return item
    def close_spider(self,spider):
        self.cur.close()
        self.connsql.close()