import re
import time

import requests
from bs4 import BeautifulSoup
from lxml import etree

HOST = "https://www.piaohua.com"


def processing_index():
    result = []
    error_times = 0
    while True:
        try:
            r = requests.get(HOST)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, "html.parser")
            a_list = soup.find_all('a')
            for a in a_list:
                # 飘花
                if '/html/' in str(a) and 'font' in str(a):
                    data = {
                        'href': 'http://www.piaohua.com' + a['href'],
                        'title': a.find_all('font')[0].text
                    }
                    result.append(data)
            break
        except Exception as e:
            time.sleep(2)
            error_times += 1
            if error_times > 10:
                break
    return result


def processing_detail(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    result = []
    # 去html标签
    dr = re.compile(r'<[^>]+>', re.S)
    # 下载链接
    for a in soup.find_all('table'):
        if 'magnet' in str(a):
            pass
        urls_download = str(a).split('"')
        for url_download in urls_download:
            url_download = dr.sub('', url_download)
            url_download = url_download.replace('>', '')
            name = dr.sub('', str(a))
            name = name.replace("[email\xa0protected]", '') \
                .replace('[飘花www.piaohua.com]', '') \
                .replace('/*  */:', '') \
                .replace('\r', '') \
                .replace('ftp://', '')
            if 'ftp' in url_download:
                if 'rmvb' in url_download \
                        or '.rm' in url_download \
                        or 'mkv' in url_download \
                        or 'mp4' in url_download \
                        or 'avi' in url_download:
                    data = {
                        'download_link': url_download,
                        'name': name,
                        'source': HOST
                    }
                    result.append(data)
            elif '.torrent' in url_download \
                    or 'thunder://' in url_download \
                    or 'ed2k' in url_download \
                    or 'magnet:?xt=urn:btih:' in url_download:
                data = {
                    'download_link': url_download,
                    'name': name,
                    'source': HOST
                }
                result.append(data)
    return result


if __name__ == '__main__':
    #
    # address = 'aaa'
    # response = requests.get('https://blockchain.info/zh-cn/rawaddr/%s' % address)
    # if response.status_code == 200:
    #     print(response.content)
    #     json_data = json.loads(response.content)
    #     for item in json_data['txs']:
    #         for out in item['out']:
    #             if out['addr'] == address:
    #                 # 表示是自己的钱包
    #                 print(out['value'])
    # processing_index(None)
    resp = requests.get('http://wenshu.court.gov.cn')
    print(resp)
    # processing_detail('https://www.piaohua.com/html/lianxuju/2017/1218/32721.html', None)
