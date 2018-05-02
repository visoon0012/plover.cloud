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

    # 存储
    # try:
    #     from_user = User.objects.get(wechat_openid=msg)
    #     wechat_req = WechatRequest.objects.get(message=msg)
    # 分析

    # 返回
    return create_reply('这是条文字消息', msg)
