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


def auto_get_movie_detail():
    # 获取所有已有的电影详情的douban_id
    douban_id_detail_list = DoubanMovie.objects.values('douban_id').all()
    douban_id_detail_list = list(douban_id_detail_list)
    len(douban_id_detail_list)
    # 获取所有没有详情的movie_simple
    douban_id_list = DoubanMovieSimple.objects.values('douban_id').all()
    print(len(douban_id_list))
    count = 0
    error_times = 0
    for douban_id in douban_id_list:
        if error_times > 20:
            break
        if douban_id not in douban_id_detail_list:
            # 不存在该资源，到豆瓣查询
            result = douban_spider.search_detail_proxy(douban_id['douban_id'])
            if result is not None and 'avatars' in result and 'rating' in result:
                count += 1
                # 保存到数据库
                DoubanMovie.objects.create(douban_id=douban_id['douban_id'], json_data=result).save()
                douban_id_detail_list.append(douban_id)
                print('已处理：{}/{}'.format(count, len(douban_id_list) - len(douban_id_detail_list)))
                error_times = 0
            else:
                error_times += 1
    #         # 不存在该资源，到豆瓣查询
    #         result = douban_spider.search_detail(douban_id)
    #         # 保存到数据库
    #         DoubanMovie.objects.create(douban_id=douban_id, json_data=result).save()


def search_resources(keyword):
    keywords = re.split("[ !！?？.。：:()（）]", keyword)
    movie_resources = MovieResource.objects
    for keyword in keywords:
        movie_resources = movie_resources.filter(Q(name__icontains=keyword) | Q(title__icontains=keyword))
    return MovieResourceSerializer(movie_resources, many=True).data
