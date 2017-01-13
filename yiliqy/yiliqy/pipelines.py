# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class YiliqyPipeline(object):

    #链接数据库
    def __init__(self):
        self.connsql = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='scrapy',charset='utf8')
        self.cur = self.connsql.cursor()


    def process_item(self, item, spider):
        text=dict(item)
        lists=text["body"].split(",")
        key="playCount"
        for l in xrange(0,len(lists)):
            if key in lists[l]:
                num=lists[l].split(":")[1]
                sql = "insert into yiliqy (num)values('" + num + "')"
                self.cur.execute(sql)
                self.connsql.commit()
        return item

    #关闭数据库
    def close_spider(self,spider):
            self.cur.close()
            self.connsql.close()
