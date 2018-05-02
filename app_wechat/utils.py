from django.core.exceptions import ObjectDoesNotExist
from wechatpy import create_reply
from wechatpy.messages import TextMessage

from app_user.models import User
from app_wechat.models import WechatRequest, UserWechatRequest


def handle_message(msg):
    """
    处理 文本 消息
    :param msg:
    :return:
    """
    # 获取用户
    try:
        from_user = User.objects.get(wechat_openid=msg.source)
    except ObjectDoesNotExist as e:
        print('此用户没有绑定')
        # 创建一个临时用户给这个人
        from_user = User.objects.create(username='WX{}'.format(msg.source), wechat_openid=msg.source)
    # 存储
    UserWechatRequest.objects.create(user=from_user, message=msg.content)
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
