# -*- coding: utf-8 -*-
import scrapy
from nba.items import zbb_vieoOrnews
from urllib import parse


# spider
# 爬取直播吧 新闻 以及视频   只有地址
# 长期更新类爬虫

# web
# 新闻展示页(多)
class TxVideoSpider(scrapy.Spider):
    name = 'zbb_news'
    allowed_domains = ['www.zhibo8.cc/nba/more.htm']
    start_urls = ['https://www.zhibo8.cc/nba/more.htm']


    start_urls_one = "https://www.zhibo8.cc/nba/more.htm?label={0}"
    team_list = [
        '勇士',
        '湖人',
        '火箭',
        '雷霆',
        '凯尔特人',
        '马刺',
        '尼克斯',
        '猛龙',
        '独行侠',
        '热火',
        '鹈鹕',
        '森林狼',
        '开拓者',
        '76人',
        '奇才',
        '老鹰',
        '其他']
    custom_settings = {
        "ITEM_PIPELINES": {
            'nba.pipelines.MysqlTwistedPipeline': 50,
            # 'nba.pipelines.DuplicatesPipeline': 1
        },
    }

    def start_requests(self):
        for i in self.team_list:
            yield scrapy.Request(url=self.start_urls_one.format(i), callback=self.parse, meta={"team_name": i})

    def parse(self, response):
        item = zbb_vieoOrnews()
        zone = response.css('.dataList ul.articleList li ')
        for i in zone:
            detail_url = i.css(' span a::attr(href)').extract()[0]
            detail_url = parse.urljoin(response.url, detail_url)
            item['detail_url'] = detail_url
            item['title'] = i.css(' span a::text').extract()[0]
            item['title_time'] = i.css(' span.postTime::text').extract()[0]
            item['team_name'] = response.meta.get("team_name", "")

            yield item
