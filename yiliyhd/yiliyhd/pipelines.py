# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
class YiliyhdPipeline(object):
    def __init__(self):
        self.connsql = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='scrapy',charset='utf8')
        self.cur = self.connsql.cursor()
    def process_item(self, item, spider):
        text=dict(item)
        num=str(text['num'][1])
        name=text['name'][0].encode("utf8")
        storename=text['storename'][0].encode("utf8")
        sql="insert into yiliyhd (num,name,storename)values('"+num+"','"+name+"','"+storename+"')"
        self.cur.execute(sql)
        self.connsql.commit()
        return item
    def close_spider(self,spider):
            self.cur.close()
            self.connsql.close()
