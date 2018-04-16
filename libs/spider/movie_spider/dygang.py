import re
from lxml import etree

import requests
from bs4 import BeautifulSoup

HOST = "http://www.dygang.com"


def processing_index(proxy):
    result = []
    r = requests.get(HOST, proxies=proxy)
    r.encoding = 'gb2312'
    selector = etree.HTML(r.text)
    a_list = selector.xpath('//td/a[@class="c2"]')
    for a in a_list:
        if 'dygang.' in str(etree.tostring(a)) and 'htm' in str(etree.tostring(a)):
            data = {
                'href': a.xpath('@href')[0],
                'title': a.text
            }
            result.append(data)
    return result


def processing_detail(url, proxy):
    result = []
    r = requests.get(url, proxies=proxy)
    r.encoding = 'gb2312'
    if r.text:
        selector = etree.HTML(r.text)
        title = selector.xpath('//tr/td/div[@class="title"]/a')[0].text
        a_list = selector.xpath('//td/a')
        for a in a_list:
            # 磁力链接
            if 'magnet' in str(etree.tostring(a)) or '.torrent' in str(etree.tostring(a)):
                data = {
                    'title': title,
                    'download_link': a.xpath('@href')[0],
                    'name': a.text,
                    'source': HOST
                }
                result.append(data)
                # 电驴和ftp链接
                # if '.mp4' in a.text or 'ftp' in a.text or 'ed2k://' in a.xpath('@href')[0]:
                #     data = {
                #         'title': title,
                #         'download_link': a.xpath('@href')[0],
                #         'name': a.text,
                #         'source': HOST
                #     }
                #     result.append(data)
    return result


if __name__ == '__main__':
    proxie = {
        'http': 'http://203.174.112.13:3128'
    }
    r = requests.get(HOST, proxies=proxie)
    r.encoding = 'gb2312'
    print(r.text)
