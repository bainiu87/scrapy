# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
class YilitbPipeline(object):
    def __init__(self):
        self.connsql = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='scrapy',charset='utf8')
        #self.connsql = MySQLdb.connect(host='192.168.1.194', port=3306, user='root', db='spider', charset='utf8')
        self.cur = self.connsql.cursor()
    def process_item(self, item, spider):
        text=dict(item)
        key="-"
        if key not in [text['sell'][0],text['eva'][0]]:
            storename=''.join(text['storename']).encode('utf8')
            sql = "insert into yilitb (eva,storename,sell)value('"+str(text['eva'][0])+"','"+storename+"','"+str(text['sell'][0])+"')"
            self.cur.execute(sql)
            self.connsql.commit()
            return item
    def close_spider(self,spider):
        self.cur.close()
        self.connsql.close()

