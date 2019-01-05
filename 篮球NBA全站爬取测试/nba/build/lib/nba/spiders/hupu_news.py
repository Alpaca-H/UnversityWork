# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from scrapy import Request
from nba.items import hupu_news
import os
from urllib import parse
from os import path


class HupuSpider(scrapy.Spider):
    name = 'hupu_news'
    allowed_domains = ['nba.hupu.com']
    start_urls = ['http://nba.hupu.com/']
    start_urls_news = "https://voice.hupu.com/nba"

    custom_settings = {
        "ITEM_PIPELINES": {'nba.pipelines.MysqlTwistedPipeline': 1},
    }

# 请求虎扑QQ登录连接，模拟登陆虎扑网站
    def login(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(
            executable_path="chromedriver.exe",chrome_options=chrome_options)
        browser.get("https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=code&client_id=222048&state=1af78ef1-a657-4863-afe1-138def82d26f&redirect_uri=https%3A%2F%2Fpassport.hupu.com%2Fpc%2Fqqcallback.action%3Ftype%3Dlogin%26jumpurl%3Dhttps%253A%252F%252Fnba.hupu.com%252F%26referer%3Dnull")
        # 模拟浏览器登陆，延时解决浏览器加载问题
        time.sleep(2)
        ss = browser.find_element_by_tag_name('iframe')
        browser.switch_to.frame(ss)
        browser.find_element_by_css_selector("a[id='switcher_plogin']").click()
        # 切换至账号密码登陆，延时解决加载问题
        time.sleep(1)
        browser.find_element_by_css_selector(
            "input[id='u']").send_keys('1097690268')
        browser.find_element_by_css_selector(
            "input[id='p']").send_keys("hzj123.4qq")
        browser.find_element_by_css_selector(
            "input[id='login_button']").click()
        # 模拟用户输入账号密码，延时解决加载问题
        time.sleep(10)

        # 获取登陆cookie值，保存本地。之后的每次请求网址都带上该cookies值进行访问
        hupu_cookies = browser.get_cookies()
        cookie_dict = {}
        import pickle
        for cookie in hupu_cookies:
            base_path = path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__))),
                'cookies')
            f = open(base_path + "/hupu/" + cookie['name'] + '.hupu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return cookie_dict

    # 获取本地cookie值，带上cookie访问start_urls_news起始网址
    def start_requests(self):
        cookie_dict = self.login()
        return [
            scrapy.Request(
                url=self.start_urls_news,
                callback=self.parse_news,
                dont_filter=True,
                cookies=cookie_dict)]

    # 根据新闻解析每条新闻的详细地址以及下一页网址的地址
    def parse_news(self, response):
        '''

        :param response:
        :return: 每条详细新闻地址回调给parse_news_detail 进行item字段提取
                 下一跳url地址回调给自身parse_news地址
        '''
        all_news_urls = response.css(
            ".news-list li .list-hd h4 a::attr(href)").extract()
        all_forums_urls = response.css(
            ".news-list li .otherInfo .other-right").extract()
        next_url = response.css("a.page-btn-prev::attr(href)").extract()
        if len(next_url) > 1:
            next_url = next_url[1]
            if next_url == '/nba/100':
                next_url = None
            else:
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse_news, dont_filter=True)
        else:

            next_url = next_url[0]
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse_news, dont_filter=True)
        for (news_url, forums_url) in zip(all_news_urls, all_forums_urls):
            yield Request(url=news_url, callback=self.parse_news_detail, dont_filter=True, meta={'forums_url': forums_url})

    def parse_news_detail(self, response):
        """

        :param response:
        :return:提取Item
        """
        item = hupu_news()
        item['title'] = response.css(
            '.artical-title h1::text').extract()[0].strip()
        item['img_url'] = response.css(
            '.artical-importantPic img::attr(src)').extract_first("None")
        item['fabu_time'] = response.css(
            "a.time span::text").extract()[0].strip()
        item['context'] = response.css(
            ".artical-main-content p::text").extract_first("None")
        item['url'] = response.url
        forums_url = response.meta['forums_url']
        if forums_url is None:
            item['forums_url'] = forums_url
        else:
            import re
            forums_url = re.search(r'([a-zA-z]+://[^\s]*)', forums_url)
            item['forums_url'] = forums_url.group(1)
        yield item
