# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import re

class YilitxPipeline(object):
    def __init__(self):
        self.connsql = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='scrapy',charset='utf8')
        self.cur=self.connsql.cursor()
    def process_item(self, item, spider):
        text=dict(item)
        strr=text['num'][0]
        key = u"\u4e07"
        if key in strr:
            num=re.findall("\d+\.?\d*",strr)
            val = str(int(float(num[0]) * 10000))
        else:
            val= str(strr)

        name=text['name'][0].encode("utf8")
        sql="insert into yilitx (name,num)values('"+name+"','"+val+"')"
        self.cur.execute(sql)
        self.connsql.commit()
        return item
    def close_spider(self,spider):
            self.cur.close()
            self.connsql.close()
