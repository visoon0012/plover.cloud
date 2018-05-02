from django.core.exceptions import ObjectDoesNotExist
from wechatpy import create_reply

from app_user.models import User
from app_wechat.models import WechatRequest


def handle_message(msg):
    """
    处理 文本 消息
    :param msg:
    :return:
    """
    # 获取消息内容
    print(msg)
    print(type(msg))
    print(type(msg.type))
    print(msg.OrderedDict())
    print(msg.OrderedDict()['FromUserName'])
    # 存储
    with User.objects.get(wechat_openid=msg['FromUserName']) as from_user:
        from_user.message = msg['Content']
        from_user.save()
        print(from_user)
    # 分析
    try:
        wechat_req = WechatRequest.objects.get(message=msg['Content'])
        return create_reply(wechat_req.response.message, msg)
    except ObjectDoesNotExist as e:
        defualt = """
        请访问下面链接获得更高级功能：\n
        http://www.plover.cloud/wechat.html?openid={}\n
        这是您的专属链接，请不要告诉他人。
        """
        return create_reply(defualt.format(msg['FromUserName']), msg)
