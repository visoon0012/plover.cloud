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
    if len(settings.CACHE['proxies']['items']) == 0 or int(time.time()) > settings.CACHE['proxies']['update'] + 3600:
        items = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        r = requests.get("http://www.xicidaili.com/%s/" % channel, headers=headers)
        r.encoding = 'utf-8'
        selector = etree.HTML(r.text)
        tr_list = selector.xpath('//tr[@class="odd"]')
        for tr in tr_list:
            td_list = tr.xpath('td')
            data = {
                'ip': td_list[1].text,
                'port': td_list[2].text,
                'type': td_list[5].text,
                'survival_time': td_list[8].text,
                'verification_time': td_list[9].text,
            }
            items.append(data)
        settings.CACHE['proxies']['items'] = items
        settings.CACHE['proxies']['update'] = int(time.time())
        return items
    else:
        print('使用缓存的代理')
        return settings.CACHE['proxies']['items']


if __name__ == '__main__':
    print(processing('nn'))
