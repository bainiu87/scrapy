# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#需要用到哪些PIPELINE 以及 执行顺序需要去setting.py文件中设置
import json
import codecs
import scrapy
import PIL
import pytesseract
import os
import urllib
import MySQLdb
import sys


#下载电话和手机图片
class DownPipeline(object):

    #管道主体处理逻辑
    def process_item(self, item, spider):
        text_1=dict(item)
        num=0
        for l in text_1["image_urls"]:
            num+=1
            urllist=str(l).split("=")
            filename=urllist[-1]+str(num)+".png"
            filepath=os.path.join("./picture/"+filename)
            urllib.urlretrieve(l,filepath)
        return item

#====================================================================================================================================

#储存到数据库中
class MysqlPipeline(object):

    #构造函数，链接数据库，创建游标
    def __init__(self):
        self.connsql = MySQLdb.connect(host='192.168.1.194', port=3306, user='root', db='spider',charset='utf8')
        self.cur = self.connsql.cursor()

    # 管道处理逻辑
    def process_item(self, item, spider):
        #配置默认编码格式，否则报错
        reload(sys)
        sys.setdefaultencoding('utf8')

        text=dict(item)

        #需要去查看下载图片管道中对图片命名规则
        filename = text["image_urls"][1].split("=")

        #使用ocr 识别图片中数字
        image_1 = PIL.Image.open("./picture/" + str(filename[-1]) + "1.png")
        vocd_1 = pytesseract.image_to_string(image_1,lang='num')
        image_2 = PIL.Image.open("./picture/" + str(filename[-1]) + "2.png")
        vocd_2 = pytesseract.image_to_string(image_2,lang='num')

        text["phone"][12] = vocd_1
        text["phone"][14] = vocd_2
        profile="|".join(text["profile"]).encode("utf8")
        phone="|".join(text["phone"][1:26]).encode("utf8")
        abstract="|".join(text["abstract"]).encode("utf8")
        imageurl="./picture/"+str(filename[-1])
        sql = "insert into soudh (profile,phone,abstract,imageurl)value('"+profile+"','"+phone+"','"+abstract+"','"+imageurl+"')"
        self.cur.execute(sql)
        self.connsql.commit()
        return item

    #析构函数，关闭连接，关闭游标
    def close_spider(self,spider):
        self.cur.close()
        self.connsql.close()

#=====================================================================================================================================


#储存到文件中
class SoudhPipeline(object):

    #管道主体程序
    def process_item(self, item, spider):
            if os.path.exists("soudh.csv"):
                self.file= codecs.open("soudh.csv","a",encoding='utf-8')
            else:
                self.file = codecs.open("soudh.csv", "wb", encoding='utf-8')
            text=dict(item)

            #需要去查看下载图片管道的命名规则
            filename=text["image_urls"][1].split("=")

            #使用ocr识别图片中的数字
            image_1=PIL.Image.open("./picture/"+str(filename[-1])+"1.png")
            vocd_1=pytesseract.image_to_string(image_1)
            image_2 = PIL.Image.open("./picture/" + str(filename[-1]) + "2.png")
            vocd_2 = pytesseract.image_to_string(image_2)


            text["phone"][12]=vocd_1
            text["phone"][14]=vocd_2
            line = json.dumps(text) + '\n'
            self.file.write(line.decode('unicode_escape'))
            return item

    #爬虫关闭时，关闭文件资源
    def close_spider(self,spider):
        self.file.close()