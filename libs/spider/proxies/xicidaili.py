import time

import requests
from lxml import etree

from config import settings


def processing(channel):
    """
    获取代理，缓存1小时
    :param channel:  nn-国内高匿/nt-国内普通/wn-国内https/wt-国内http
    :return:
    """
    if len(settings.CACHE['proxies']['items']) == 0 or int(time.time()) > settings.CACHE['proxies']['update'] + 60 * 60 * 0.5:
        items_http = []
        items_https = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        r = requests.get("http://www.xicidaili.com/%s/1" % channel, headers=headers)
        r.encoding = 'utf-8'
        selector = etree.HTML(r.text)
        tr_list = selector.xpath('//tr[@class="odd"]')
        for tr in tr_list:
            td_list = tr.xpath('td')
            data = {
                'ip': td_list[1].text,
                'port': td_list[2].text,
                'type': str(td_list[5].text).lower(),
                'survival_time': td_list[8].text,
                'verification_time': td_list[9].text,
            }
            if data['type'] == 'http':
                items_http.append(data)
            if data['type'] == 'https':
                items_https.append(data)
        items = []
        print(len(items_http), len(items_https))
        for item in range(len(items_https) if len(items_http) > len(items_https) else len(items_http)):
            proxies = {
                "%s" % items_http[item]['type']: "%s://%s:%s" % (items_http[item]['type'], items_http[item]['ip'], items_http[item]['port']),
                "%s" % items_https[item]['type']: "%s://%s:%s" % (items_https[item]['type'], items_https[item]['ip'], items_https[item]['port']),
            }
            try:
                r2 = requests.get("http://api.douban.com/v2/movie/subject/27021220", headers=headers, proxies=proxies)
                r2.encoding = r2.apparent_encoding
                print(r2.text)
                if 'avatars' in r2.text and 'rating' in r2.text:
                    print('新增代理')
                    items.append(proxies)
            except Exception as e:
                print(e)
        settings.CACHE['proxies']['items'] = items
        settings.CACHE['proxies']['update'] = int(time.time())
        return items
    else:
        print('使用缓存的代理')
        return settings.CACHE['proxies']['items']


def processing2(channel, page=1):
    """
    获取代理，缓存1小时
    :param page: 页码数
    :param channel:  nn-国内高匿/nt-国内普通/wn-国内https/wt-国内http
    :return:
    """
    if len(settings.CACHE['proxies']['items']) == 0 or int(time.time()) > settings.CACHE['proxies']['update'] + 60 * 60 * 1:
        items = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        r = requests.get("http://www.xicidaili.com/{}/{}".format(channel, page), headers=headers)
        r.encoding = 'utf-8'
        selector = etree.HTML(r.text)
        tr_list = selector.xpath('//tr[@class="odd"]')
        for tr in tr_list:
            td_list = tr.xpath('td')
            data = {
                'ip': td_list[1].text,
                'port': td_list[2].text,
                'type': str(td_list[5].text).lower(),
                'survival_time': td_list[8].text,
                'verification_time': td_list[9].text,
            }
            items.append(data)
        result = []
        count = 0
        for item in items:
            count += 1
            proxies = {
                "http": "http://%s:%s" % (item['ip'], item['port']),
                "https": "https://%s:%s" % (item['ip'], item['port']),
            }
            try:
                r2 = requests.get("https://api.douban.com/v2/movie/subject/27021220", headers=headers, proxies=proxies, timeout=3)
                r2.encoding = r2.apparent_encoding
                if 'avatars' in r2.text and 'rating' in r2.text:
                    print('新增代理')
                    result.append(proxies)
            except Exception as e:
                pass
        print('可用的代理数量：{}'.format(len(result)))
        settings.CACHE['proxies']['items'] = result
        settings.CACHE['proxies']['update'] = int(time.time())
        return result
    else:
        return settings.CACHE['proxies']['items']


if __name__ == '__main__':
    print(processing('nn'))
