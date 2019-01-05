# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import datetime
from scrapy.loader import ItemLoader

from nba.settings import SQL_DATE_FORMAT,SQL_DATETIME_FORMAT
from nba.utils.common import extract_num, extract_num_include_dot
import re


def clean_other(value):
    return value.replace('\\', '').strip()

class NbaItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor  = TakeFirst()
    default_input_processor  = MapCompose(clean_other)




class Nba_coach(scrapy.Item):
    pass
#     birth_day  = scrapy.Field()
#     birth_city  = scrapy.Field()
#     high_school   = scrapy.Field()
#     university  = scrapy.Field()
#     shengya  = scrapy.Field()
#     changguisai  = scrapy.Field()
#     jihousai  = scrapy.Field()
#     zongjuesai  = scrapy.Field()
#     zongguanjun  = scrapy.Field()
#     url  = scrapy.Field()
#     coach_name  = scrapy.Field(input_processor=MapCompose(clean_other))
#
#     def get_insert_sql(self):
#         insert_sql  = """
#             insert into nba_coach(birth_day,coach_name)
#             VALUES (%s,%s)
#         """
#         params  = (self["birth_day"],self["coach_name"])
#
#         return insert_sql, params






#虎扑新闻
class hupu_news(scrapy.Item):
    title  = scrapy.Field()
    img_url =scrapy.Field()
    fabu_time =scrapy.Field()
    context = scrapy.Field()
    url  = scrapy.Field()
    forums_url  = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into hupu_nba_news(title,img_url,fabu_time,context,url,forums_url)
            VALUES (%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE title=VALUES(title)
        """
        params  = (self["title"],self["img_url"],self["fabu_time"],self["context"],self["url"],self["forums_url"])

        return insert_sql, params


#教练战绩
class nba_standings(scrapy.Item):
    id =scrapy.Field()
    coach_name  = scrapy.Field()
    mingrentang = scrapy.Field()
    zuijiao_coach = scrapy.Field()
    zongguanjun = scrapy.Field()
    zongjuesai = scrapy.Field()
    jihousai = scrapy.Field()
    saijishu = scrapy.Field()
    changguisaishenglv = scrapy.Field()
    changci = scrapy.Field()
    shengchang = scrapy.Field()
    fuchang = scrapy.Field()
    jihousaishenglv = scrapy.Field()
    changci1 = scrapy.Field()
    shengchang1 = scrapy.Field()
    fuchang1 = scrapy.Field()
    def get_insert_sql(self):
        insert_sql  = """
            insert into coach_standings(coach_name,id,mingrentang,zuijiao_coach,zongguanjun,zongjuesai,jihousai,saijishu,changguisaishenglv,changci,shengchang,fuchang,jihousaishenglv,changci1,shengchang1,fuchang1)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['coach_name'],self["id"],self["mingrentang"],self["zuijiao_coach"],self["zongguanjun"],self["zongjuesai"],
                  self["jihousai"],self["saijishu"],self["changguisaishenglv"],self["changci"],self["shengchang"],self["fuchang"],
                  self["jihousaishenglv"], self["changci1"], self["shengchang1"], self["fuchang1"])

        return insert_sql, params

#教练详情
class nba_coach_detail(scrapy.Item):
    coach_name  = scrapy.Field()
    birth_day  = scrapy.Field()
    birth_city = scrapy.Field()
    high_school = scrapy.Field()
    university = scrapy.Field()
    shengya = scrapy.Field()
    changguisai = scrapy.Field()
    jihousai = scrapy.Field()
    zongjuesai = scrapy.Field()
    zongguanjun = scrapy.Field()
    zuijia_coach = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into coach_detail(coach_name,birth_day,birth_city,high_school,university,shengya,changguisai,jihousai,zongjuesai,zongguanjun,zuijia_coach)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['coach_name'],self["birth_day"],self["birth_city"],self["high_school"],self["university"],self["shengya"],
                  self["changguisai"],self["jihousai"],self["zongjuesai"],self["zongguanjun"],self["zuijia_coach"])

        return insert_sql, params


class Tx_nba_1718_jq_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1718_jq_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1718_jq_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()


    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1718_jq_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1718_cg_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()


    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1718_cg_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1718_cg_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1718_cg_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1718_jh_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1718_jh_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1718_jh_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()


    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1718_jh_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1617_jq_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1617_jq_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1617_jq_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()


    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1617_jq_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1617_cg_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()


    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1617_cg_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1617_cg_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1617_cg_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1617_jh_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1617_jh_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1617_jh_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1617_jh_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1516_jq_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1516_jq_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1516_jq_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()


    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1516_jq_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1516_cg_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()


    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1516_cg_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1516_cg_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1516_cg_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1516_jh_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1516_jh_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1516_jh_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1516_jh_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1819_jq_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1819_jq_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1819_jq_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()


    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1819_jq_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1819_cg_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()


    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1819_cg_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1819_cg_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1819_cg_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1819_jh_cj(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1819_jh_cj(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


class Tx_nba_1819_jh_qb(scrapy.Item):
    paiming  = scrapy.Field()
    qiuyuan = scrapy.Field()
    qiudui = scrapy.Field()
    defen_selected = scrapy.Field()
    chushou = scrapy.Field()
    mingzhong = scrapy.Field()
    chushou3 = scrapy.Field()
    mingzhong3 = scrapy.Field()
    faci = scrapy.Field()
    falv = scrapy.Field()
    lanban = scrapy.Field()
    qlanban = scrapy.Field()
    hlanban = scrapy.Field()
    zhugong = scrapy.Field()
    qiangduan = scrapy.Field()
    gaimao = scrapy.Field()
    shiwu = scrapy.Field()
    fangui = scrapy.Field()
    changci = scrapy.Field()
    shangchang = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
            insert into Tx_nba_1819_jh_qb(paiming,qiuyuan,qiudui,defen_selected,chushou,mingzhong,
                                    chushou3,mingzhong3,faci,falv,lanban,qlanban,hlanban,zhugong,qiangduan,gaimao,shiwu,
                                    fangui,changci,shangchang)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params  = (self['paiming'],self["qiuyuan"],self["qiudui"],self["defen_selected"],self["chushou"],self["mingzhong"],
                  self["chushou3"],self["mingzhong3"],self["faci"],self["falv"],self["lanban"],
                  self["qlanban"],self["hlanban"],self["zhugong"],self["qiangduan"],self["gaimao"],self["shiwu"],self["fangui"],
                  self["changci"],self["shangchang"])

        return insert_sql, params


#直播吧新闻
class zbb_vieoOrnews(scrapy.Item):
    title  = scrapy.Field()
    detail_url  = scrapy.Field()
    title_time  = scrapy.Field()
    team_name  = scrapy.Field()
    def get_insert_sql(self):
        insert_sql  = """
            insert into zbb_news(title,detail_url,title_time,team_name)
            VALUES (%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE title=VALUES(title),detail_url=VALUES(detail_url),title_time=VALUES(title_time),team_name=VALUES(team_name)
        """
        params  = (self["title"], self["detail_url"], self["title_time"], self["team_name"])

        return insert_sql, params


#新浪新闻
class xl_videoOrnews(scrapy.Item):
    title  = scrapy.Field()
    title_time  = scrapy.Field()
    detail_url  = scrapy.Field()
    team_name =scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
               insert into xl_news(title,detail_url,title_time,team_name)
               VALUES (%s,%s,%s,%s)
           """


        params  = (self["title"], self["detail_url"], self["title_time"], self["team_name"])

        return insert_sql, params


#腾讯 nba视频
class tx_video(scrapy.Item):
    video_time  = scrapy.Field()
    video_id  = scrapy.Field()
    video_img  = scrapy.Field()
    video_playUrl  = scrapy.Field()
    video_num  = scrapy.Field()
    video_title  = scrapy.Field()
    true_url  = scrapy.Field()
    video_theme  = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
                 insert into tx_video(video_time,video_id,video_img,video_playUrl,video_num,video_title,true_url,video_theme)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                  ON DUPLICATE KEY UPDATE video_title=VALUES(video_title)
             """
        params  = (self["video_time"], self["video_id"], self["video_img"], self["video_playUrl"], self["video_num"], self["video_title"], self["true_url"],self['video_theme'])

        return insert_sql, params


class player_info(scrapy.Item):
    team_img = scrapy.Field()
    imgurl = scrapy.Field()
    c_name = scrapy.Field()
    e_name = scrapy.Field()
    player_number = scrapy.Field()
    weizhi = scrapy.Field()
    shengao = scrapy.Field()
    tizhong = scrapy.Field()
    shengri = scrapy.Field()
    hetong = scrapy.Field()
    hetong2 = scrapy.Field()
    start_urls = scrapy.Field()

    def get_insert_sql(self):
        insert_sql  = """
                 insert into player_info(team_img,imgurl,c_name,e_name,player_number,weizhi,shengao,tizhong,shengri,hetong,hetong2,start_urls)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 ON DUPLICATE KEY UPDATE team_img=VALUES(team_img), imgurl=VALUES(imgurl),
                  e_name=VALUES(e_name), player_number=VALUES(player_number), weizhi=VALUES(weizhi), 
                  shengao=VALUES(shengao),tizhong=VALUES(tizhong),shengri=VALUES(shengri),hetong=VALUES(hetong),
                  hetong2=VALUES(hetong2),start_urls=VALUES(start_urls)
             """
        params = (self["team_img"], self["imgurl"], self["c_name"], self["e_name"], self["player_number"], self["weizhi"], self["shengao"], self["tizhong"], self["shengri"], self["hetong"], self["hetong2"], self["start_urls"])
        return insert_sql, params




class zhihuItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    #获得list[0]方法1
    #活动list[0]方法2   zhihu_id =  "".join(self["zhihu_id"])
    #活动list[0]方法3   zhihu_id =  self["zhihu_id"][0]


class zhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
            insert into zhihu_question(zhihu_id,topics,url,title,content,answer_num,comments_num,watch_user_num,click_num,crawl_time)
            VALUES (%s, %s, %s,%s,%s, %s, %s,%s,%s,%s) 
        """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url =  self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        try:
            answer_num = extract_num("".join(self["answer_num"]))
        except BaseException:
            answer_num = 0
        comments_num = extract_num("".join(self["comments_num"]))
        if len(self["watch_user_num"]) == 2:
            watch_user_num_click = self["watch_user_num"]
            watch_user_num = extract_num_include_dot(watch_user_num_click[0])
            click_num = extract_num_include_dot(watch_user_num_click[1])
        else:
            watch_user_num_click = self["watch_user_num"]
            watch_user_num = extract_num_include_dot(watch_user_num_click[0])
            click_num = 0
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (zhihu_id,topics,url,title,content,answer_num,comments_num,watch_user_num,click_num,crawl_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    #知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parse_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
            insert into zhihu_answer(zhihu_id,url,question_id,author_id,content,parse_num,comments_num,create_time,update_time,crawl_time)
            VALUES (%s, %s, %s,%s,%s, %s, %s,%s,%s,%s) 
        """
        # create_time = datetime.datetime.fromtimestamp(self["create_time"].strftime(SQL_DATETIME_FORMAT))
        # update_time = datetime.datetime.fromtimestamp(self["update_time"].strftime(SQL_DATETIME_FORMAT))

        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["parse_num"],
            self["comments_num"], self['create_time'], self['update_time'],
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params