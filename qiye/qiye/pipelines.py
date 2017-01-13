# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#需要用那个PIPELINE 需要去setting.py配置
import codecs
import json
import os
import MySQLdb

#将数据存储到mysql数据库中
class MysqlPipeline(object):

    #开启爬虫时运行连接数据库，创建游标
    def open_spider(self, spider):
        self.connsql = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='scrapy',charset='utf8')
        self.cur = self.connsql.cursor()

    #管道处理
    def process_item(self, item, spider):
        lists=dict(item)
        info="|".join(lists["info"]).encode("utf8")
        profile="|".join(lists["profile"]).encode("utf8")
        supply="|".join(lists["supply"]).encode("utf8")
        sql = "insert into qiye (info,profile,supply)value('"+info+"','"+profile+"','"+supply+"')"
        self.cur.execute(sql)
        self.connsql.commit()
        return item


    #爬虫关闭时，关闭数据库，游标
    def close_spider(self,spider):
        self.cur.close()
        self.connsql.close()


#============================================================================================================================================================

#将数据存储到re.csv文件中
class TextPipeline(object):

    #管道处理
    def process_item(self,item,spider):
        if os.path.exists("re.csv"):
            self.file = codecs.open("re.csv", "a", encoding='utf-8')
        else:
            self.file = codecs.open("re.csv", "wb", encoding='utf-8')
        text=dict(item)
        line = json.dumps(text) + '\n'
        self.file.write(line.decode('unicode_escape'))
        return item

    #爬虫关闭时将文件资源关闭
    def close_spider(self,spider):
        self.file.close()