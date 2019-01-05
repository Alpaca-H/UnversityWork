# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from nba.items import Tx_nba_1617_jq_cj, Tx_nba_1617_jq_qb, Tx_nba_1617_cg_cj, Tx_nba_1617_cg_qb, Tx_nba_1617_jh_cj, Tx_nba_1617_jh_qb
from scrapy import Request
import time


# 静态爬虫，数据更新很慢，基本不用更新
# 1617数据

class TxNbaSpider(scrapy.Spider):
    name = 'Tx_nba_1617'
    allowed_domains = [
        'nba.stats.qq.com/stats/detail/?order=defen&type=player']
    start_urls = [
        'http://nba.stats.qq.com/stats/detail/?order=defen&type=player']

    # broswer = webdriver.Chrome("E:\LinuxShare\chromedriver.exe")

    custom_settings = {
        "ITEM_PIPELINES": {'nba.pipelines.MysqlTwistedPipeline': 1},
    }

    def login(self):
        self.broswer.get(self.start_urls[0])
        self.change("#season-select", "#season-select ul li", index=2)
        self.broswer.find_element_by_css_selector(
            'div.pages ul li.selected').click()
        time.sleep(2)
        text = self.broswer.page_source
        return text

    def change(self, first_e, second_e, index):
        """
        改变右上角下拉框参数，比如我要选择2016-2017项的，那我的index应该就是2
        :param first_e: 第一个选择器，固定dropdownlist
        :param second_e:第二个选择器，选择下拉列表中的内容
        :param index:返回第几个
        :return:
        """
        # 跳转4页结束之后，会读取不到全部这个下拉框，要使用JS向上拉
        self.broswer.execute_script("window.scrollBy(0,-5000)")
        time.sleep(2)
        self.broswer.find_element_by_css_selector(first_e).click()
        time.sleep(2)
        self.broswer.find_elements_by_css_selector(second_e)[index].click()
        time.sleep(2)
        text = self.broswer.page_source
        return text

    def right_under(self):
        time.sleep(3)
        self.broswer.find_element_by_css_selector(
            'div.pages ul li.selected+li').click()
        time.sleep(2)
        text = self.broswer.page_source
        return text

    def start_requests(self):
        text = self.login()
        yield Request(callback=self.parse_1617_jqs_cj, dont_filter=True, url=self.start_urls[0], meta={'tt': text})

    # 季前赛-场均   -->季前赛全部
    def parse_1617_jqs_cj(self, response):
        item = Tx_nba_1617_jq_cj()
        # 登陆，获取pagesource
        text = response.meta['tt']
        response = Selector(text=text)
        keywords = response.xpath(
            "//ul[@class='content']/li[1]/div/@class|//ul[@class='content']/li[1]/span/@class|//ul[@class='content']/li[1]/div/span/@class").extract()
        # 循环获取数据，筛选
        for i in range(1, 51):
            xx = "//ul[@class='content']/li[{0}]/div/text()|//ul[@class='content']/li[{1}]/span/text()|//ul[@class='content']/li[{2}]/div/span/text()".format(
                i, i, i)
            content = response.xpath(xx).extract()
            content.remove(' ')
            content.remove(' ')
            dict1 = dict(zip(keywords, content))
            for k, v in dict1.items():
                k = k.replace(' ', '_')
                if k == 'paiming_first':
                    k = 'paiming'
                item[k] = v
            time.sleep(0.5)
            yield item
        if response.xpath(
                "//div[@class='pages']/ul/li[@class='selected']/text()").extract_first() == '4':
            # 跳转全部
            text = self.change(
                first_e="#statistics-select",
                second_e="#statistics-select  li",
                index=1)
            yield Request(callback=self.Tx_nba_1617_jq_qb, dont_filter=True, url=self.start_urls[0], meta={'tt': text})
            pass
        else:
            text = self.right_under()
            yield Request(callback=self.parse_1617_jqs_cj, dont_filter=True, url=self.start_urls[0], meta={'tt': text})

    # 季前赛-全部   -->  常规全部
    def Tx_nba_1617_jq_qb(self, response):
        item = Tx_nba_1617_jq_qb()
        # 登陆，获取pagesource
        text = response.meta['tt']
        response = Selector(text=text)
        keywords = response.xpath(
            "//ul[@class='content']/li[1]/div/@class|//ul[@class='content']/li[1]/span/@class|//ul[@class='content']/li[1]/div/span/@class").extract()
        # 循环获取数据，筛选
        for i in range(1, 50):
            xx = "//ul[@class='content']/li[{0}]/div/text()|//ul[@class='content']/li[{1}]/span/text()|//ul[@class='content']/li[{2}]/div/span/text()".format(
                i, i, i)
            content = response.xpath(xx).extract()
            content.remove(' ')
            content.remove(' ')
            dict1 = dict(zip(keywords, content))
            for k, v in dict1.items():
                k = k.replace(' ', '_')
                if k == 'paiming_first':
                    k = 'paiming'
                item[k] = v
            time.sleep(0.5)
            yield item
        if response.xpath(
                "//div[@class='pages']/ul/li[@class='selected']/text()").extract_first() == '4':
            # 季前赛全部 完成，跳转常规赛
            text = self.change(
                first_e="#matchType-select",
                second_e="#matchType-select  li",
                index=1)
            yield Request(callback=self.Tx_nba_1617_cg_qb, dont_filter=True, url=self.start_urls[0], meta={'tt': text})
        else:
            text = self.right_under()
            yield Request(callback=self.Tx_nba_1617_jq_qb, dont_filter=True, url=self.start_urls[0], meta={'tt': text})

    # 常规赛-全部  -->  常规场均
    def Tx_nba_1617_cg_qb(self, response):
        item = Tx_nba_1617_cg_qb()
        # 登陆，获取pagesource
        text = response.meta['tt']
        response = Selector(text=text)
        keywords = response.xpath(
            "//ul[@class='content']/li[1]/div/@class|//ul[@class='content']/li[1]/span/@class|//ul[@class='content']/li[1]/div/span/@class").extract()
        # 循环获取数据，筛选
        for i in range(1, 50):
            xx = "//ul[@class='content']/li[{0}]/div/text()|//ul[@class='content']/li[{1}]/span/text()|//ul[@class='content']/li[{2}]/div/span/text()".format(
                i, i, i)
            content = response.xpath(xx).extract()
            content.remove(' ')
            content.remove(' ')
            dict1 = dict(zip(keywords, content))
            for k, v in dict1.items():
                k = k.replace(' ', '_')
                if k == 'paiming_first':
                    k = 'paiming'
                item[k] = v
            time.sleep(0.5)
            yield item
        if response.xpath(
                "//div[@class='pages']/ul/li[@class='selected']/text()").extract_first() == '4':
            # 常规赛全部完成，跳转常规赛场均
            text = self.change(
                first_e="#statistics-select",
                second_e="#statistics-select  li",
                index=0)
            yield Request(callback=self.Tx_nba_1617_cg_cj, dont_filter=True, url=self.start_urls[0], meta={'tt': text})
        else:
            text = self.right_under()
            yield Request(callback=self.Tx_nba_1617_cg_qb, dont_filter=True, url=self.start_urls[0], meta={'tt': text})

    # 常规赛-场均  -->季后场均
    def Tx_nba_1617_cg_cj(self, response):
        item = Tx_nba_1617_cg_cj()
        # 登陆，获取pagesource
        text = response.meta['tt']
        response = Selector(text=text)
        keywords = response.xpath(
            "//ul[@class='content']/li[1]/div/@class|//ul[@class='content']/li[1]/span/@class|//ul[@class='content']/li[1]/div/span/@class").extract()
        # 循环获取数据，筛选
        for i in range(1, 50):
            xx = "//ul[@class='content']/li[{0}]/div/text()|//ul[@class='content']/li[{1}]/span/text()|//ul[@class='content']/li[{2}]/div/span/text()".format(
                i, i, i)
            content = response.xpath(xx).extract()
            content.remove(' ')
            content.remove(' ')
            dict1 = dict(zip(keywords, content))
            for k, v in dict1.items():
                k = k.replace(' ', '_')
                if k == 'paiming_first':
                    k = 'paiming'
                item[k] = v
            time.sleep(0.5)
            yield item
        if response.xpath(
                "//div[@class='pages']/ul/li[@class='selected']/text()").extract_first() == '4':
            # 常规赛场均完成，跳转季后赛场均
            text = self.change(
                first_e="#matchType-select",
                second_e="#matchType-select  li",
                index=2)
            yield Request(callback=self.Tx_nba_1617_jh_cj, dont_filter=True, url=self.start_urls[0],
                          meta={'tt': text})
        else:
            text = self.right_under()
            yield Request(callback=self.Tx_nba_1617_cg_cj, dont_filter=True, url=self.start_urls[0],
                          meta={'tt': text})

    # 季后赛-场均  -->季候全部
    def Tx_nba_1617_jh_cj(self, response):
        item = Tx_nba_1617_jh_cj()
        # 登陆，获取pagesource
        text = response.meta['tt']
        response = Selector(text=text)
        keywords = response.xpath(
            "//ul[@class='content']/li[1]/div/@class|//ul[@class='content']/li[1]/span/@class|//ul[@class='content']/li[1]/div/span/@class").extract()
        # 循环获取数据，筛选
        for i in range(1, 50):
            xx = "//ul[@class='content']/li[{0}]/div/text()|//ul[@class='content']/li[{1}]/span/text()|//ul[@class='content']/li[{2}]/div/span/text()".format(
                i, i, i)
            content = response.xpath(xx).extract()
            content.remove(' ')
            content.remove(' ')
            dict1 = dict(zip(keywords, content))
            for k, v in dict1.items():
                k = k.replace(' ', '_')
                if k == 'paiming_first':
                    k = 'paiming'
                item[k] = v
            time.sleep(0.5)
            yield item
        if response.xpath(
                "//div[@class='pages']/ul/li[@class='selected']/text()").extract_first() == '4':
            # 季后赛场均完成，跳转季后赛全部
            text = self.change(
                first_e="#statistics-select",
                second_e="#statistics-select  li",
                index=1)
            yield Request(callback=self.Tx_nba_1617_jh_qb, dont_filter=True, url=self.start_urls[0], meta={'tt': text})
        else:
            text = self.right_under()
            yield Request(callback=self.Tx_nba_1617_jh_cj, dont_filter=True, url=self.start_urls[0], meta={'tt': text})

    # 季后赛-全部  -->结束
    def Tx_nba_1617_jh_qb(self, response):
        item = Tx_nba_1617_jh_qb()
        text = response.meta['tt']
        response = Selector(text=text)
        keywords = response.xpath(
            "//ul[@class='content']/li[1]/div/@class|//ul[@class='content']/li[1]/span/@class|//ul[@class='content']/li[1]/div/span/@class").extract()
        # 循环获取数据，筛选
        for i in range(1, 50):
            xx = "//ul[@class='content']/li[{0}]/div/text()|//ul[@class='content']/li[{1}]/span/text()|//ul[@class='content']/li[{2}]/div/span/text()".format(
                i, i, i)
            content = response.xpath(xx).extract()
            content.remove(' ')
            content.remove(' ')
            dict1 = dict(zip(keywords, content))
            for k, v in dict1.items():
                k = k.replace(' ', '_')
                if k == 'paiming_first':
                    k = 'paiming'
                item[k] = v
            time.sleep(0.5)
            yield item
        if response.xpath(
                "//div[@class='pages']/ul/li[@class='selected']/text()").extract_first() == '4':
            # 季后赛场均完成，跳转季后赛全部
            # 17-18全部完成,关闭浏览器
            self.broswer.close()
        else:
            text = self.right_under()
            yield Request(callback=self.Tx_nba_1617_jh_qb, dont_filter=True, url=self.start_urls[0], meta={'tt': text})
