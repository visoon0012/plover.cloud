import logging

from app_movie.models import DoubanMovie, DoubanMovieSimple
from app_movie.utils import get_movie_simple
from libs.spider.movie_spider import douban_spider

logger = logging.getLogger(__name__)


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
            print(result)
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


def auto_test():
    logger.warning('自动任务调起')
