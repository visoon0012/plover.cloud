import random

import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin

from libs.spider.proxies import xicidaili


def search_novel(engine, proxy, title):
    engines = [
        search_novel_xxshu5(proxy, title)
    ]
    return engines[engine]


def search_chapter(engine, proxy, url):
    engines = [
        search_chapter_detail(proxy, url)
    ]
    return engines[engine]


def search_novel_xxshu5(proxy, title):
    """
    获取小说名和章节列表
    :param proxy:
    :param title:
    :return:
    """
    host = 'http://www.xxshu5.com'
    title = ''.join(lazy_pinyin(title))
    url = host + '/%s/' % title
    r = requests.get(url, proxies=proxy)
    soup = BeautifulSoup(r.text, "html.parser")
    info = soup.find(id='info')
    if info is None:
        raise Exception('搜索不到这本小说')
    info_p_list = info.find_all('p')
    intro = soup.find(id='intro')
    fmimg = soup.find(id='fmimg')
    cover = fmimg.img['src']
    if not str(cover).startswith('http'):
        cover = host + cover
    chapters = soup.find(id='list').find_all('dd')
    novel = {
        'title': info.h1.text,
        'author': info_p_list[0].text.split('：')[1],
        'new': info_p_list[2].text.split('：')[1],
        'new_time': info_p_list[3].text.split('：')[1],
        'intro': intro.p.text,
        'cover': cover,
        'link': url
    }
    novel_chapters = []
    for chapter in chapters:
        data = {
            'host': host,
            'title': chapter.a.text,
            'link': host + chapter.a['href']
        }
        novel_chapters.append(data)
    return novel, novel_chapters


def search_chapter_detail(proxy, url):
    """
    获取小说章节正文
    :param proxy:
    :param url:
    :return:
    """
    r = requests.get(url, proxies=proxy)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, "html.parser")
    # 搜索正文
    content = soup.find(id='content') or soup.find(id='BookText')
    return content.text


if __name__ == '__main__':
    # 1.获取代理
    proxies = xicidaili.processing('nn')
    tmp = random.sample(proxies, 1)[0]
    proxy = {
        "%s" % tmp['type']: "%s://%s:%s" % (tmp['type'], tmp['ip'], tmp['port'])
    }
    url = 'http://www.soduso.com/go_113230745.aspx?t=0B5B054DB3D537F4795A508493DBBD72067962A807110C03A71ED4434B7CD1293AF1565A4C8C4EA197267DC9CED4835D602831372553A1EC'
    print(search_chapter_detail(proxy, url))
