# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import urljoin
from nba.items import nba_standings, nba_coach_detail



class NbaCoachSpider(scrapy.Spider):
    name = 'nba_coach'
    allowed_domains = ['stat-nba.com/query_coach.php']
    start_urls = ['http://stat-nba.com/query_coach.php/']

    custom_settings = {
        "ITEM_PIPELINES": {'nba.pipelines.MysqlTwistedPipeline': 1},
    }

    keywords = {'birth_day': '出生日期', 'birth_city': '出生城市',
                "high_school": '高中', "university": '大学', 'shengya': '执教生涯',
                "changguisai": '常规赛', 'jihousai': '季后赛', 'zongjuesai': '总决赛',
                'zongguanjun': '总冠军', 'zuijia_coach': '最佳教练'}

    def parse(self, response):
        # 获取表头
        sss = response.css(".stat_box thead tr th::text").extract()
        # 返回教练列表
        for i in range(0, 13):
            next_url = "http://stat-nba.com/query_coach.php/?page={0}#label_show_result".format(
                i)
            yield Request(url=next_url, dont_filter=True, callback=self.parse_standings)

    def parse_standings(self, response):
        '''
        分析教练战绩
        :param response:
        :return: 回调一个教练详情给parse_coach
        '''
        item = nba_standings()
        for i in range(1, 21):
            # 获取教练详情列表
            select = "//table[@class='stat_box']/tbody/tr[{0}]/td/text()|//table[@class='stat_box']/tbody/tr[{1}]/td/a/text()".format(
                i, i)
            ss = response.xpath(select).extract()
            item['id'] = ss[0]
            item['coach_name'] = ss[1]
            item['mingrentang'] = ss[2]
            item['zuijiao_coach'] = ss[3]
            item['zongguanjun'] = ss[4]
            item['zongjuesai'] = ss[5]
            item['jihousai'] = ss[6]
            item['saijishu'] = ss[7]
            # 去掉胜率的%
            item['changguisaishenglv'] = ss[8].replace('%', '')
            item['changci'] = ss[9]
            item['shengchang'] = ss[10]
            item['fuchang'] = ss[11]
            item['jihousaishenglv'] = ss[12].replace('%', '')
            item['changci1'] = ss[13]
            item['shengchang1'] = ss[14]
            item['fuchang1'] = ss[15]
            import time
            time.sleep(0.5)
            yield item
        coach_detail_url = response.css(
            '.stat_box tbody tr td a::attr(href)').extract()
        for i in coach_detail_url:
            yield Request(url=urljoin(response.url, i), callback=self.parse_coach, dont_filter=True)

    def parse_coach(self, response):
        item = nba_coach_detail()
        coach_name = response.xpath("//div[@class='name']/text()").extract()[0]
        detail = response.xpath(
            "//div[@class='detail']/div[@class='row']/text()|//div[@class='detail']/div[@class='row']/div[@class='column']/text()").extract()
        for i in range(len(detail)):
            detail[i] = detail[i].replace(
                '\xa0',
                '').replace(
                '\u3000',
                '').replace(
                ':',
                '')
        detail_dict = dict(zip(detail[0::2], detail[1::2]))
        for i in self.keywords.values():
            if i not in detail_dict.keys():
                detail_dict[i] = None
        for k, v in self.keywords.items():
            item[k] = detail_dict[v]
        item['coach_name'] = coach_name
        yield item
