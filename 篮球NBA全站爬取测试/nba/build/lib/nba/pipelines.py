# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from qiniu import BucketManager
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi  # 可以将mysqldb中的一些操作变成异步化的一些操作

from qiniu import Auth, put_file, etag, put_data
from urllib.parse import urljoin

qiniu_yuming = "http://pjie39vqz.bkt.clouddn.com/{0}"
# 需要填写你的 Access Key 和 Secret Key
access_key = 'ufomitGGHohBvhG_9Pz9BefpPnAxeDeyigke-UPR'
secret_key = 'TSfTMcw747J4vYnbWdpJ4gRfn6MsYUWpenBCoheL'
bucket_name = 'nba-rtf'  # 要上传的空间


class NbaPipeline(object):
    def process_item(self, item, spider):
        return item


# 数据过多的时候使用异步插入
# 使用异步的插入Twisted


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, setting):
        dbparms = dict(
            host=setting["MYSQL_HOST"],
            db=setting["MYSQL_DBNAME"],
            passwd=setting["MYSQL_PASSWD"],
            user=setting["MYSQL_USER"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twiced将mysql插入变成异步
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 处理异常

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行插入操作
        # 根据不同的item 构建不同的sql语句 并插入到数据库中
        # 方法1:根据item的名字来判断
        # if item.__class__.__name__ == "JobBoleArticleItem":
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


# 上传七牛云文件
def get_img(url, key):
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    ret, info = bucket.fetch(url, bucket_name, key)
    return urljoin(qiniu_yuming, key)


class fetchImgPipeline(object):
    def process_item(self, item, spider):
        url = item['video_img']
        name = item['video_id']
        s = get_img(url, key=name)
        item['video_img'] = s
        return item

# 去重Pipeline


class DuplicatesPipeline(object):
    """
    去重
    """
    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        name = item['title']
        if name in self.book_set:
            raise DropItem("Duplicate book found:%s" % item)

        self.book_set.add(name)
        return item
