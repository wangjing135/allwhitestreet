# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllwhitestreetItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    nums = scrapy.Field()
    times = scrapy.Field()
    author = scrapy.Field()
    uid = scrapy.Field()
    allwenzhang = scrapy.Field()
    fensi = scrapy.Field()

    # def get_insert_sql(self):
    #     insert_sql = """insert into huaerjie(name,url,num,time)
    #                                     values
    #                                     (%s,%s,%s,%s)"""
    #     insert_sqls = """insert into author(uid,author,allwenzhang,fensi)
    #                                                 values
    #                                                 (%s,%s,%s,%s)"""
    #     paramss = (self['uid'], self['author'], self['allwenzhang'], self['fensi'])
    #     params = (self['title'],self['url'],self['nums'],self['times'])
    #     return insert_sql, params,insert_sqls, paramss

