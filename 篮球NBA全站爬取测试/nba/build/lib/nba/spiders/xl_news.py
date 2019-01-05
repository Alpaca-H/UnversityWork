# -*- coding: utf-8 -*-
import scrapy
from nba.items import xl_videoOrnews

# spider
# 爬取新浪Nba新闻
# 长期更新类爬虫

# web
# 新闻展示页(多)


class XlVideoSpider(scrapy.Spider):
    name = 'xl_news'
    allowed_domains = ['sports.sina.com.cn/nba/']
    start_urls = ['http:/sports.sina.com.cn/nba/']
    team_dict = {"勇士": "25", "火箭": "1", "湖人": "5"}
    start_urls_one = "http://sports.sina.com.cn/nba/{0}.shtml"

    custom_settings = {
        "ITEM_PIPELINES": {
            'nba.pipelines.MysqlTwistedPipeline': 100,
            'nba.pipelines.DuplicatesPipeline': 1
        },
    }

    def start_requests(self):
        for k, v in self.team_dict.items():
            yield scrapy.Request(url=self.start_urls_one.format(v), callback=self.parse, meta={"team_name": k})

    def parse(self, response):
        item = xl_videoOrnews()
        news_lists = response.css("#leftbot #right")
        for i in news_lists:
            for j in range(len(i.css('a::text').extract())):
                item['title_time'] = i.css(
                    'span:not(.selected):not(.noselected)::text').extract()[j]
                item['detail_url'] = i.css('a::attr(href)').extract()[j]
                url = i.css('a::attr(href)').extract()[j]
                item['team_name'] = response.meta.get("team_name", "")
                item['title'] = i.css('a::text').extract()[j]
                yield item
