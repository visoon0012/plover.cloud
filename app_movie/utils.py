import json
import re
from time import sleep

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from app_movie.models import DoubanMovieSimple, MovieResource, DoubanMovie
from app_movie.serializer import MovieResourceSerializer
from libs.spider.movie_spider import douban_spider


def get_movie_simple(m_type, m_tag):
    result = douban_spider.search_list(m_type, m_tag, 500, 0)
    if result:
        # 重置当前已经有的数据level为0
        DoubanMovieSimple.objects.filter(douban_tag=m_tag, douban_type=m_type).update(level=0)
        # 循环更新
        movies = json.loads(result)['subjects']
        level = len(movies)
        for movie in movies:
            level -= 1
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
            # 资源数计算
            keywords = re.split("[ !！?？.。：:()（）・·]", movie['title'])
            movie_resources = MovieResource.objects.values('id')
            for keyword in keywords:
                movie_resources = movie_resources.filter(Q(name__icontains=keyword) | Q(title__icontains=keyword))
            if movie_simple.douban_type == 'movie':
                movie_resources = movie_resources.exclude(name__iregex='连载至[0-9]+')
                movie_resources = movie_resources.exclude(name__iregex='[\u4e00-\u9fa5]*{}[0-9]+'.format(movie['title']))
                movie_resources = movie_resources.exclude(title__iregex='连载至[0-9]+')
                movie_resources = movie_resources.exclude(title__iregex='[\u4e00-\u9fa5]*{}[0-9]+'.format(movie['title']))
            movie_simple.resources = movie_resources.count()
            movie_simple.save()
        return Response({'message': 'ok'})
    else:
        return Response({'message': 'none data'}, status=status.HTTP_400_BAD_REQUEST)


def search_resources(keyword):
    keywords = re.split("[ !！?？.。：:()（）]", keyword)
    movie_resources = MovieResource.objects
    for keyword in keywords:
        movie_resources = movie_resources.filter(Q(name__icontains=keyword) | Q(title__icontains=keyword))
    return MovieResourceSerializer(movie_resources, many=True).data
