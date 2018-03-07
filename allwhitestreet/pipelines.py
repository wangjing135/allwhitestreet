# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class AllwhitestreetPipeline(object):
    #def process_item(self, item, spider):
        #return item
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
from scrapy import log

class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            port= settings['MYSQL_PORT'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    # def do_insert(self, cursor, item):
    #     # 执行具体的插入
    #     # 根据不同的item 构建不同的sql语句并插入到mysql中
    #     insert_sql, params = item.get_insert_sql()
    #     insert_sqls, paramss = item.get_insert_sql()
    #     print(insert_sql, params)
    #     cursor.execute(insert_sql, params)
    #     cursor.execute(insert_sqls, paramss)
    #
    # def do_inserts(self, cursor, item):
    #     # 执行具体的插入
    #     # 根据不同的item 构建不同的sql语句并插入到mysql中
    #     insert_sqls, paramss = item.get_insert_sqls()
    #     print(insert_sqls, paramss)
    #     cursor.execute(insert_sqls, paramss)
    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        try:
            SQL = """insert into huaerjie(name,url,num,time)
                                values
                                (%s,%s,%s,%s)"""
            cursor.execute(SQL, (item['title'],item['url'],item['nums'],item['times']))
            SQL = """insert into author(uid,author,allwenzhang,fensi)
                                            values
                                            (%s,%s,%s,%s)"""
            cursor.execute(SQL, (item['uid'], item['author'], item['allwenzhang'], item['fensi']))
        except Exception as e:
            print('***** Logging failed with this error:', str(e))
            log.msg('***** Logging failed with this error:', str(e), level=log.INFO, spider=None)
    # def do_inserts(self, cursor, item):
    #     try:
    #         SQL = """insert into author(uid,author,allwenzhang,fensi)
    #                             values
    #                             (%s,%s,%s,%s)"""
    #         cursor.execute(SQL, (item['uid'],item['author'],item['allwenzhang'],item['fensi']))
    #     except Exception as e:
    #         print('***** Logging failed with this error:', str(e))
        print(item['title'],item['uid'],item['author'],item['allwenzhang'],item['fensi'],item['times'])