
# -*- coding:utf-8 -*-
__author__ = 'hzj'


import hashlib
import re



def get_md5(url):
    if isinstance(url,str):  #在python3当中str就是unicode形式
        url = url.encode('utf-8')
    else:
        url = url

    m = hashlib.md5()
    m.update(url)

    return m.hexdigest()

def extract_num(text):
    #从字符串中提取数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def extract_num_include_dot(text):
    # 从包含,的字符串中提取出数字
    text_num = text.replace(',', '')
    try:
        nums = int(text_num)
    except:
        nums = -1
    return nums

# if __name__ == "__main__":
#     print(get_md5("http://jobbole.com".encode('utf-8')))

