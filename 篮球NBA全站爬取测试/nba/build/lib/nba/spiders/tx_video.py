# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from nba.items import tx_video
import datetime

# spider
# 长期更新类爬虫

# web
# Top100


class TxVideoSpider(scrapy.Spider):
    name = 'tx_video'
    allowed_domains = ['v.qq.com/detail/5/52363.html']
    start_urls = ['http://v.qq.com/detail/5/52363.html/']
    start_urls_one = "http://s.video.qq.com/get_playsource?id=52363&plat=2&type=4&data_type=3&video_type=4&year=2018&month={0}&plname=qq&otype=json&callback=_jsonp_8_841a&_t=1540868247149"
    start_urls_two = "http://s.video.qq.com/get_playsource?id=882&plat=2&type=4&data_type=3&video_type=4&year=2018&month={0}&plname=qq&otype=json&callback=_jsonp_2_ad1c&_t=1541645200562"
    month_list = datetime.datetime.now().month

    custom_settings = {
        "ITEM_PIPELINES": {
            'nba.pipelines.MysqlTwistedPipeline': 50,
            'nba.pipelines.fetchImgPipeline': 1},
    }

    def start_requests(self):
        for i in range(1, self.month_list + 1):
            yield Request(url=self.start_urls_one.format(i), callback=self.parse, dont_filter=True, meta={"theme": "NBA全场集锦"})
        for i in range(1, self.month_list):
            yield Request(url=self.start_urls_two.format(i), callback=self.parse, dont_filter=True, meta={"theme": "NBA全场回放"})

    def parse(self, response):
        video_lists = json.loads(response.text[13:].strip("(").strip(")"))
        PlaylistItem = video_lists['PlaylistItem']
        videoPlayLists = PlaylistItem['videoPlayList']
        for videoPlayList in videoPlayLists:
            item = tx_video()
            item['video_time'] = videoPlayList['episode_number']
            item['video_id'] = videoPlayList['id']
            item['video_img'] = videoPlayList['pic']
            item['video_playUrl'] = videoPlayList['playUrl']
            item['video_num'] = videoPlayList['thirdLine']
            item['video_title'] = videoPlayList['title']
            item['video_theme'] = response.meta.get("theme", "")
            url = videoPlayList['playUrl']
            list = url.split("?")
            list1 = list[0].split(".html")
            list2 = list[1].split("=")
            true_url = list1[0] + "/" + list2[1] + ".html"
            item['true_url'] = true_url
            yield item
