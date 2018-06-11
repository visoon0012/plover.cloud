import json

import requests
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from app_user.models import User
from app_wechat.utils import handle_message

WECHAT_TOKEN = 'plovercloud'


@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'error'
        response = HttpResponse(echo_str, content_type="text/plain")
        return response
    elif request.method == 'POST':
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = handle_message(msg)
        elif msg.type == 'image':
            reply = create_reply('这是条图片消息，暂时还不能处理该类型消息', msg)
        elif msg.type == 'voice':
            reply = create_reply('这是条语音消息，暂时还不能处理该类型消息', msg)
        else:
            # 关注/取消关注的时候
            reply = handle_message(msg)
        response = HttpResponse(reply.render(), content_type="application/xml")
        return response
    else:
        print('不存在的方法')


@csrf_exempt
def wechat_openid(request):
    """获取小程序openid并注册系统"""
    appid = 'wxfa64d5c4005bd355'
    secret = 'a1719c25d2b003192a5fe20e61339a1f'
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'code' not in data:
            return Response('参数错误', status=status.HTTP_400_BAD_REQUEST)
        # 通过 code 获取 openid
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(appid, secret, data['code'])
        r = requests.get(url)
        openid = json.loads(r.text)['openid']
        # 获取或者创建用户
        user, created = User.objects.get_or_create(username='WX{}'.format(openid), wechat_openid=openid)
        if created:
            user.set_password(openid)
        else:
            user.nickname = data['user']['nickName']
        user.save()
        return HttpResponse(openid)
