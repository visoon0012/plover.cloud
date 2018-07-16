import json
from time import sleep

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app_poem.models import Poem, Author, Dynasty, Tag
from libs.spider.poem_spider import gushiwen


@csrf_exempt
def processing_detail(request):
    base_url = 'https://www.gushiwen.org/shiwen/default.aspx?page=%s&type=0&id=0'
    id = 0
    poem = Poem.objects.order_by('-get_id').first()
    id = poem.get_id
    error_times = 0
    while True:
        # 判断错误次数
        if error_times > 100:
            break
        # 处理
        id += 1
        print('正在处理：%s' % id)
        try:
            try:
                poem = Poem.objects.get(get_id=id)
                print('已经有该记录...%s' % poem.title)
                continue
            except ObjectDoesNotExist as e:
                pass
            # 获取信息
            sleep(3)
            data = gushiwen.processing(base_url, id)
            # 保存到数据库
            try:
                author = Author.objects.get(name=data['author'])
            except ObjectDoesNotExist as e:
                author = Author.objects.create(name=data['author'])
                author.save()
            try:
                dynasty = Dynasty.objects.get(name=data['dynasty'])
            except ObjectDoesNotExist as e:
                dynasty = Dynasty.objects.create(name=data['dynasty'])
                dynasty.save()
            tag_objects = []
            for tag in data['tags']:
                try:
                    tag = Tag.objects.get(name=tag)
                except ObjectDoesNotExist as e:
                    tag = Tag.objects.create(name=tag)
                    tag.save()
                tag_objects.append(tag)
            poem = Poem.objects.create(get_id=id,
                                       title=data['title'],
                                       content=data['content'],
                                       author=author,
                                       dynasty=dynasty)
            poem.save()
            poem.tags = tag_objects
            poem.save()
            # 重置错误次数
            error_times = 0
            print('成功')
        except Exception as e:
            print(e)
            error_times += 1
            print('失败')
    return HttpResponse(json.dumps({'message': '处理完毕'}), content_type="application/json", status=200)
