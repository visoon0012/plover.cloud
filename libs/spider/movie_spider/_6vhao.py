import re

import requests
from bs4 import BeautifulSoup

HOST = "http://www.6vhao.com"


def processing_index(soup):
    result = []
    a_list = soup.find_all('a')
    for a in a_list:
        # 6vhao
        if 'hao6v' in str(a):
            print(str(a))
            if len(str(a['href'])) < 5:
                continue
            else:
                dr = re.compile(r'<[^>]+>', re.S)
                title = dr.sub('', a.text)
                data = {
                    'href': a['href'],
                    'title': title
                }
                result.append(data)
    return result


def processing_detail(url):
    result = []
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    # 去html标签
    dr = re.compile(r'<[^>]+>', re.S)
    # 标题
    title = str(soup.title)
    title = dr.sub('', title)
    title = title.replace('免费下载', '').replace('最新电影', '').replace('电影港', '').replace('_', '')
    # 下载链接
    for a in soup.find_all('a'):
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
                        'title': title,
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
                    'title': title,
                    'download_link': url_download,
                    'name': name,
                    'source': HOST
                }
                result.append(data)
    return result
