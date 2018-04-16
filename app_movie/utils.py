import json
from time import sleep

from rest_framework import status
from rest_framework.response import Response

from app_movie.models import DoubanMovieSimple
from libs.spider.movie_spider import douban_spider


def get_movie_simple(m_type, m_tag):
    result = douban_spider.search_list(m_type, m_tag, 500, 0)
    if result:
        # 重置当前已经有的数据level为0
        DoubanMovieSimple.objects.filter(douban_tag=m_tag, douban_type=m_type).update(level=0)
        # 循环更新
        movies = json.loads(result)['subjects']
        movies.reverse()
        level = 0
        for movie in movies:
            level += 1
            movie_simple, created = DoubanMovieSimple.objects.get_or_create(
                douban_id=movie['id'],
                douban_tag=m_tag,
                douban_type=m_type
            )
            if movie['rate']:
                movie_simple.rate = movie['rate']
            if movie['cover']:
                movie_simple.cover = movie['cover']
            if movie['cover_x']:
                movie_simple.cover_x = movie['cover_x']
            if movie['cover_y']:
                movie_simple.cover_y = movie['cover_y']
            movie_simple.title = movie['title']
            movie_simple.is_new = movie['is_new']
            movie_simple.url = movie['url']
            movie_simple.level = level
            movie_simple.save()
        return Response({'message': 'ok'})
    else:
        return Response({'message': 'none data'}, status=status.HTTP_400_BAD_REQUEST)


def auto_get_movie_simple():
    get_movie_simple('movie', '热门')
    get_movie_simple('movie', '最新')
    get_movie_simple('tv', '热门')
    get_movie_simple('tv', '国产剧')
    get_movie_simple('tv', '美剧')
    get_movie_simple('tv', '日剧')
    get_movie_simple('tv', '韩剧')
