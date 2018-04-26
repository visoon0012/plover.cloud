import json
import random

import requests

from libs.spider.proxies import xicidaili


def get_soup(url):
    try:
        proxies = xicidaili.processing('nn')
        tmp = random.sample(proxies, 1)[0]
        proxy = {
            "%s" % tmp['type']: "%s://%s:%s" % (tmp['type'], tmp['ip'], tmp['port'])
        }
        response = requests.get(url, proxies=proxy)
        return response.text
    except Exception as e:
        print(e)


def search_list(_type, tag, movie_type, page):
    url = 'https://movie.douban.com/j/search_subjects?type=%s&tag=%s&sort=recommend&page_limit=%s&page_start=%s' \
          % (_type, tag, movie_type, page)
    print(url)
    return get_soup(url)


def search_detail(movie_id):
    url = 'http://api.douban.com/v2/movie/subject/%s' % str(movie_id)
    print(url)
    return get_soup(url)


if __name__ == '__main__':
    # print(search_list('movie', '热门', 20, 0))
    print(search_detail(24751763))
