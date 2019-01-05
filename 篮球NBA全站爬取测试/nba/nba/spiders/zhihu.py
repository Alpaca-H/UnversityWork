import json
import os
import re
from os import path
from urllib import parse
import scrapy
from scrapy.loader import ItemLoader
from nba.items import zhihuQuestionItem,ZhihuAnswerItem
from datetime import datetime


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']
    custom_settings = {
        "ITEM_PIPELINES": {
            'nba.pipelines.MysqlTwistedPipeline': 100,
        },
    }
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={1}&offset={2}&sort_by=default"
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/68.0.3440.106 Safari/537.36"
    }

    def parse(self, response):
        """
        # 提取出html中所有页面的url
        #筛选出url格式为/question/xxx 后下载之后直接进入解析函数

        :param response:
        :return:
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)

        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 提取到内容就交给parse_question处理详情页
                request_url = match_obj.group(1)
                yield scrapy.Request(url=request_url,headers=self.headers,callback=self.parse_question)
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url=url,headers=self.headers,callback=self.parse)


    def parse_question(self, response):
        # 处理question页面，从页面中提取出具体的question item
        # 处理新版本
        if "QuestionHeader-title" in response.text:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))
            item_loader = ItemLoader(item=zhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id",question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")
            question_item = item_loader.load_item()
        else:
            # 处理知乎旧的版本
            # 处理老版本页面的item提取
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))
            item_loader = ItemLoader(item=zhihuQuestionItem(), response=response)
            # item_loader.add_css("title", ".zh-question-title h2 a::text")
            # 由于title标题会放在a标签里面或者span标签里面，所以这里要使用到xpath方法，来获取内容
            item_loader.add_xpath("title","//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")
            item_loader.add_xpath("watch_user_num", "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")
            question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers,
                             callback=self.parse_answer)
        yield question_item

    def parse_answer(self,response):
        # 处理question的answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            # 279554654

            answer_item["url"] = answer["url"]
            # https://www.zhihu.com/api/v4/questions/279554654

            answer_item["question_id"] = answer["question"]["id"]
            # 279554654

            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None

            answer_item["parse_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]

            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    def start_requests(self):
        cookie_dict=self.login()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict, headers=self.headers)]

    def login(self):
        """
        #登录知乎，并且获取cookies值保存到本地之后关闭浏览器

        :return: cookies
        """
        from selenium import webdriver
        import time
        browser = webdriver.Chrome(executable_path="E:\LinuxShare\chromedriver.exe")

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            "13175509596")
        time.sleep(1)
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
            "hzjqq12.3")
        time.sleep(2)
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(2)

        zhihu_cookies = browser.get_cookies()
        cookie_dict = {}
        import pickle
        for cookie in zhihu_cookies:
            base_path = path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cookies')
            f = open(base_path + "/zhihu/" + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return cookie_dict