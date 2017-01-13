# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import MySQLdb

class YilijdPipeline(object):

    def __init__(self):
        self.connsql = MySQLdb.connect(host='localhost', port=3306, user='root',passwd='root', db='scrapy', charset='utf8')
        self.cur = self.connsql.cursor()

    def process_item(self, item, spider):
        text = dict(item)
        strs = text["num"][0]
        key = u"\u4e07"
        #判断万是否存在，入存在则需要*10000
        if key in strs:
            #正则提取数字
            b = re.findall("\d+\.?\d*", strs)
            val = str(int(float(b[0]) * 10000))
            sql = "insert into yilijd (num)values('" + val + "')"
            self.cur.execute(sql)
            self.connsql.commit()
        else:
            b = re.findall("\d+\.?\d*", strs)
            val = b[0]
            sql = "insert into yilijd (num)values('" + val + "')"
            self.cur.execute(sql)
            self.connsql.commit()
        return item

    def close_spider(self,spider):
        self.cur.close()
        self.connsql.close()

