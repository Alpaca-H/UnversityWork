# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy import Request
import json
from nba.items import Sc

class ScSpider(scrapy.Spider):
    name = 'sc'
    allowed_domains = ['tiyu.baidu.com']
    start_urls = ['http://tiyu.baidu.com/']

    import_words = "from=self"
    import_url = "http://tiyu.baidu.com/{0}"

    custom_settings = {
        "ITEM_PIPELINES": {'nba.pipelines.MysqlTwistedPipeline': 50}
    }

    def get_time(self):
        now_time = datetime.datetime.now().date()  #  03 04
        now_day = int(str(now_time).split('-')[2])

        after_day = now_day + 2
        after_time = str(now_time).split('-')[0] + '-' + str(now_time).split('-')[1] + '-' + str(after_day)  # 04 05

        # if now_day == 1 or now_day == 2 or now_day == 3:
        #     forward_day = 28
        #     forward_month = int(str(now_time).split('-')[1])
        #     if forward_month == 1 or forward_month == 2 or forward_month == 3:
        #         forward_month = 12
        #         forward_time = '2018' + '-' + str(forward_month) + '-' + str(
        #             forward_day)  # 31 30 29   月份为12
        #     else:
        #         forward_day = now_day - 3
        #         forward_time = '2018' + '-' + str(now_time).split('-')[1] + '-' + str(
        #             forward_day)  # 31 30 29
        #         return after_time, forward_time
        # else:
        #     forward_day = now_day - 3
        #     forward_time = '2018'+ '-' + str(now_time).split('-')[1] + '-' + str(
        #         forward_day)  # 31 30 29

        forward_day = now_day - 2
        forward_time = str(now_time).split('-')[0] + '-' + str(now_time).split('-')[1] + '-' + str(forward_day)  # 1 2
        return after_time, forward_time

    def start_requests(self):
        now_time = datetime.datetime.now().date()  # 02 03
        after_time, forward_time = self.get_time()
        forward_url = "http://tiyu.baidu.com/api/match/NBA/live/date/{0}/direction/after?{1}".format(forward_time,self.import_words)
        after_url =  "http://tiyu.baidu.com/api/match/NBA/live/date/{0}/direction/after?{1}".format(after_time,self.import_words)
        now_url = "http://tiyu.baidu.com/api/match/NBA/live/date/{0}/direction/after?{1}".format(now_time,self.import_words)
        yield Request(url=now_url, callback=self.parse,meta={'after_url':after_url,'forward_url':forward_url})

    def parse(self, response):   # 3 4
        after_url = response.meta.get('after_url')
        forward_url = response.meta.get('forward_url')
        jsonList = json.loads(response.text)
        for i in range(2):
            Qlist = jsonList['data'][i]['list']
            for qlist in Qlist:
                sc = Sc()
                sc['datatime'] = jsonList['data'][i]['time']
                sc['startTime'] = qlist['startTime']
                sc['matchName'] = qlist['matchName']
                sc['link'] = self.import_url.format(qlist['link'])
                sc['leftLogo'] = qlist['leftLogo']['logo']
                sc['leftName'] = qlist['leftLogo']['name']
                sc['rightLogo'] = qlist['rightLogo']['logo']
                sc['rightName'] = qlist['rightLogo']['name']
                sc['vsLine'] = qlist['vsLine']
                yield sc
        yield Request(url=after_url, callback=self.after_parse,meta={'forward_url':forward_url})

    def after_parse(self,response):  # 5 6
        forward_url = response.meta.get('forward_url')
        jsonList = json.loads(response.text)
        for i in range(2):
            Qlist = jsonList['data'][i]['list']
            for qlist in Qlist:
                sc = Sc()
                sc['datatime'] = jsonList['data'][i]['time']
                sc['startTime'] = qlist['startTime']
                sc['matchName'] = qlist['matchName']
                sc['link'] = self.import_url.format(qlist['link'])
                sc['leftLogo'] = qlist['leftLogo']['logo']
                sc['leftName'] = qlist['leftLogo']['name']
                sc['rightLogo'] = qlist['rightLogo']['logo']
                sc['rightName'] = qlist['rightLogo']['name']
                sc['vsLine'] = qlist['vsLine']
                yield sc
        yield Request(url=forward_url, callback=self.forward_parse)

    def forward_parse(self, response):  # 1 2
        jsonList = json.loads(response.text)
        for i in range(2):
            Qlist = jsonList['data'][i]['list']
            for qlist in Qlist:
                sc = Sc()
                sc['datatime'] = jsonList['data'][i]['time']
                sc['startTime'] = qlist['startTime']
                sc['matchName'] = qlist['matchName']
                sc['link'] = self.import_url.format(qlist['link'])
                sc['leftLogo'] = qlist['leftLogo']['logo']
                sc['leftName'] = qlist['leftLogo']['name']
                sc['rightLogo'] = qlist['rightLogo']['logo']
                sc['rightName'] = qlist['rightLogo']['name']
                sc['vsLine'] = qlist['vsLine']
                yield sc



