# -*- coding:utf-8 -*-
__author__ = 'hzj'
from qiniu import Auth, put_file, etag,put_data
from urllib.parse import  urljoin
qiniu_yuming = "http://phpmwjs7v.bkt.clouddn.com/{0}"
access_key = 'ufomitGGHohBvhG_9Pz9BefpPnAxeDeyigke-UPR'  # 需要填写你的 Access Key 和 Secret Key
secret_key = 'TSfTMcw747J4vYnbWdpJ4gRfn6MsYUWpenBCoheL'
bucket_name = 'nba-rtf2'  # 要上传的空间

from qiniu import BucketManager
# def get_img():
#     q = Auth(access_key, secret_key)
#     bucket = BucketManager(q)
#     url = 'http://wx4.sinaimg.cn/mw690/7cc829d3gy1fqz3p82kbhj20xc0hi40j.jpg'
#     key = 'xxx.jpg'
#     ret, info = bucket.fetch(url, bucket_name, key)
#     print(ret['key'])
#     return qiniu_yuming.format(ret['key'])

def get_img(url,key):
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    ret, info = bucket.fetch(url, bucket_name, key)
    return urljoin(qiniu_yuming,key)


if __name__ == '__main__':
    get_img()
