import datetime
import random
from time import sleep

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from app_book import spider_engines
from app_book.models import NovelFork, Novel, NovelChapter
from libs.spider.proxies import xicidaili


def search_novel(title):
    """
    按照标题搜索小说
    :param title:
    :return:
    """
    # 1.获取代理
    proxies = xicidaili.processing('nn')
    tmp = random.sample(proxies, 1)[0]
    proxy = {
        "%s" % tmp['type']: "%s://%s:%s" % (tmp['type'], tmp['ip'], tmp['port'])
    }
    # 获取数据
    novel, novel_chapters = spider_engines.search_novel(0, proxy, title)
    return novel, novel_chapters


def search_novel_chapter(url):
    """
    获取章节内容
    :param url:
    :return:
    """
    # 1.获取代理
    proxies = xicidaili.processing('nn')
    tmp = random.sample(proxies, 1)[0]
    proxy = {
        "%s" % tmp['type']: "%s://%s:%s" % (tmp['type'], tmp['ip'], tmp['port'])
    }
    return spider_engines.search_chapter(0, proxy, url)


def auto_update_fork():
    """
    自更新已经Fork的小说
    :return:
    """
    novel_forks = NovelFork.objects.values('novel__id', 'novel__title', 'novel__updated_time').filter(used=True).annotate(forks=Count('novel'))
    # 更新目录
    for item in novel_forks:
        now_time = datetime.datetime.now()
        if (now_time - item['novel__updated_time']).seconds > 60 * 60 * 6:  # 大于6个小时更新一次
            _novel, chapters = search_novel(item['novel__title'])
            for chapter in chapters:
                try:
                    NovelChapter.objects.get(title=chapter['title'], novel_id=item['novel__id'])
                except ObjectDoesNotExist as e:
                    novel_chapters = NovelChapter.objects.create(novel_id=item['novel__id'], title=chapter['title'], link=chapter['link'])
                    novel_chapters.save()
            novel = Novel.objects.get(id=item['novel__id'])
            novel.save()


def auto_download():
    """
    自动下载小说章节正文
    :return:
    """
    novel_chapters = NovelChapter.objects.filter(content='')
    count = 0
    for novel_chapter in novel_chapters:
        try:
            sleep(3)
            count += 1
            content = search_novel_chapter(novel_chapter['link'])
            novel_chapter.content = content
            novel_chapter.save()
        except Exception as e:
            print(e)
    print('下载完毕，新增: %s' % count)
    return count


if __name__ == '__main__':
    # print(''.join(lazy_pinyin('神话版三国')))
    # novel, novel_chapters = search_novel('放开那个女巫')
    # print(novel)
    # print(novel_chapters)
    # data = search_novel_chapter('http://www.xxshu5.com/fangkainagenvwu/1356304/')
    # print(data)
    # url = 'http://www.soduso.com/gogourl_4356866.aspx'
    # r = requests.get(url)
    # r.encoding = 'gb2312'
    # print(r.text)
    auto_update_fork()
