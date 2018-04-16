import json

from django.http import HttpResponse
from lxml import etree

import requests

from app_spider.models import Proxy


def processing(request):
    """
    获取代理
    channel:  nn-国内高匿/nt-国内普通/wn-国内https/wt-国内http
    :return:
    """
    channel = 'nn'
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
        try:
            proxy = Proxy(**data)
            proxy.save()
        except Exception as e:
            pass
    return HttpResponse(json.dumps({'message': 'ok'}), content_type="application/json")


if __name__ == '__main__':
    processing('nn')
