import json
import random

import requests

from libs.spider.proxies import xicidaili


def get_soup(url):
    try:
        proxies = xicidaili.processing2('nn', page=1)
        proxy = random.choice(proxies)
        response = requests.get(url, proxies=proxy, timeout=5)
        return response.text
    except Exception as e:
        return None


def search_list(_type, tag, movie_type, page):
    url = 'https://movie.douban.com/j/search_subjects?type=%s&tag=%s&sort=recommend&page_limit=%s&page_start=%s' \
          % (_type, tag, movie_type, page)
    response = requests.get(url)
    return response.text


def search_detail(movie_id):
    url = 'http://douban.uieee.com/v2/movie/subject/%s' % str(movie_id)
    response = requests.get(url)
    return response.text


def search_detail_proxy(movie_id):
    url = 'https://api.douban.com/v2/movie/subject/%s' % str(movie_id)
    return get_soup(url)


if __name__ == '__main__':
    # print(search_list('movie', '热门', 20, 0))
    print(search_detail(24751763))
