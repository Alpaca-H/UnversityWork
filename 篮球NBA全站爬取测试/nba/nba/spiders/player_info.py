# -*- coding: utf-8 -*-
import scrapy
from nba.items import player_info


# 获取球员信息，并且将照片存储到七牛云
# fetchImgPipeline 注释掉了。
# 节省流量QAQ


class PlayerInfoSpider(scrapy.Spider):
    name = 'player_info'
    allowed_domains = ['nba.hupu.com']
    start_urls = ['https://nba.hupu.com/players']

    custom_settings = {
        # "ITEM_PIPELINES": {'nba.pipelines.fetchImgPipeline': 1,},
        # "ITEM_PIPELINES": {'nba.pipelines.MysqlTwistedPipeline': 10},
    }

    def parse(self, response):
        start_urls = response.css(
            ".players_left .players_list li  span a::attr(href)").extract()
        team_imgs = response.css(
            ".players_left .players_list li img::attr(src)").extract()
        for start_url in start_urls:
            for team_img in team_imgs:
                yield scrapy.Request(url=start_url, callback=self.list_info, meta={"start_urls": start_url, "team_img": team_img})

    def list_info(self, response):
        item = player_info()
        ss = response.css(".players_table  tbody tr")
        for tr in ss[1:]:
            item['team_img'] = response.meta.get("team_img", "")
            item['start_urls'] = response.meta.get("start_urls", "")
            item['imgurl'] = tr.css(
                ".td_padding a img::attr(src)").extract()[0]
            item['c_name'] = tr.css(".left b a::text").extract()[0]
            item['e_name'] = tr.css(".left p b::text").extract()[0]
            item['player_number'] = tr.css("td")[2].extract()
            item['weizhi'] = tr.css("td").extract()[3]
            item['shengao'] = tr.css("td").extract()[4]
            item['tizhong'] = tr.css("td").extract()[5]
            item['shengri'] = tr.css("td").extract()[6]
            item['hetong'] = str(tr.css(".left::text").extract()[3:])
            item['hetong2'] = str(tr.css(".left b::text").extract()[1:])
            import time
            time.sleep(0.5)
            yield item
