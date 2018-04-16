import json
import re
import uuid

import jieba as jieba
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app_spider.models import Job
from libs.spider.job import gxrc


@csrf_exempt
def processing_list(request):
    """广西人才网数据"""
    result = []
    try:
        page = 0
        while True:
            page += 1
            print(page)
            url = 'http://s.gxrc.com/sJob?schType=1&district=2&posType=5480,5483,5481,5484&page=%s&pageSize=20&orderType=3&listValue=1' % page
            items = gxrc.processing_list(url)
            for item in items:
                try:
                    job = Job(**item)
                    job.uuid = uuid.uuid3(uuid.NAMESPACE_URL, item['href'])
                    job.save()
                except Exception as e:
                    pass
            # 没有数据了，退出
            if len(items) == 0:
                break
        return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'message': 'error'}), content_type="application/json", status=400)


@csrf_exempt
def processing_data(request):
    """数据处理"""
    items = Job.objects.values("job_name", "company_name", "amount", "nature").all()
    total_data = {
        "job_keywords": [],
        "company_keywords": [],
    }
    for item in items:
        total_data['job_keywords'].extend(jieba.cut(re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+", "", item['job_name'])))
        total_data['company_keywords'].extend(jieba.cut(re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+", "", item['company_name'])))
    # 词频分析
    job_dict = {}
    for keyword in total_data['job_keywords']:
        if keyword in job_dict.keys():
            job_dict[keyword] += 1
        else:
            job_dict[keyword] = 1
    job_dict = sorted(job_dict.items(), key=lambda x: x[1], reverse=True)  # 排序
    for item in job_dict:
        print(item)
    #
    # word_dict = {}
    # for item in total_data['company_keywords']:
    #     for item2 in item:
    #         if item2 not in word_dict:
    #             word_dict[item2] = 1
    #         else:
    #             word_dict[item2] += 1
    # # 排序
    # sorted(dict2list(word_dict), key=lambda x: x[1], reverse=True)
    # for key in word_dict:
    #     print(key + ' ' + str(word_dict[key]))
    return HttpResponse(json.dumps([]), content_type="application/json")


def dict2list(dic: dict):
    """将字典转化为列表"""
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst
