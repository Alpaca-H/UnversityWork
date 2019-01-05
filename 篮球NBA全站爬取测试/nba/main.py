# -*- coding:utf-8 -*-
__author__ = 'hzj'


from  scrapy.cmdline import execute


import sys
import  os

# sys.path.append("E:\LinuxShare\ArticleSpider")  这里是windows下面的路径，但是这样做一旦我们更换了其他的系统比如mac linux就会出现问题
sys.path.append(os.path.dirname(os.path.abspath(__file__))) #这里的__file__指的就是main.py这个文件 abspat获取到该文件的绝对路径 \
# 并且使用dirname得到他上一级的目录，在windows下也就是E:\LinuxShare\ArticleSpider

execute(["scrapy","crawl","sc"])

