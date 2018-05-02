from django.core.exceptions import ObjectDoesNotExist
from wechatpy import create_reply
from wechatpy.messages import TextMessage

from app_user.models import User
from app_wechat.models import WechatRequest


def handle_message(msg):
    """
    处理 文本 消息
    :param msg:
    :return:
    """
    # 获取消息内容
    # 存储
    with User.objects.get(wechat_openid=msg.source) as from_user:
        from_user.message = msg.content
        from_user.save()
    # 分析
    try:
        wechat_req = WechatRequest.objects.get(message=msg.content)
        return create_reply(wechat_req.response.message, msg)
    except ObjectDoesNotExist as e:
        defualt = """
        请访问下面链接获得更高级功能：\n
        http://www.plover.cloud/wechat.html?openid={}\n
        这是您的专属链接，请不要告诉他人。
        """
        return create_reply(defualt.format(msg.source), msg)
