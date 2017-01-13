# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
class YiliykPipeline(object):

    def __init__(self):
        self.conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='root',db='scrapy',charset='utf8')
        self.cur=self.conn.cursor()

    def process_item(self, item, spider):
        text=dict(item)
        name="".join(text["name"]).encode("utf8")
        url=text['url'][0].encode("utf8")
        num=str(text['num'][0].replace(",",""))
        sql="insert into yiliyk (name,url,num)value('"+name+"','"+url+"','"+num+"')"
        self.cur.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()