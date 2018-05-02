from django.core.exceptions import ObjectDoesNotExist
from wechatpy import create_reply

from app_movie.utils import search_resources
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
        # 创建一个临时用户给这个人
        from_user = User.objects.create(username='WX{}'.format(msg.source), wechat_openid=msg.source)
    # 存储
    UserWechatRequest.objects.create(user=from_user, message=msg.content)
    # 分析
    if str(msg.content)[0:2] in ['搜索', ]:
        return handle_cmd(msg)
    else:
        try:
            wechat_req = WechatRequest.objects.get(message=msg.content)
            return create_reply(wechat_req.response.message, msg)
        except ObjectDoesNotExist as e:
            default = """请访问下面链接获得更高级功能：\nhttp://www.plover.cloud/wechat.html?openid={}\n这是您的专属链接，请不要告诉他人。\n如需帮助请输入：帮助。"""
            return create_reply(default.format(msg.source), msg)


def handle_cmd(msg):
    """
    处理 指令
    :param msg:
    :return:
    """
    cmds = str(msg.content).split('-')
    if len(cmds) == 3:
        if cmds[0] == '搜索':
            if cmds[1] == '电影':
                result = search_resources(cmds[2])
                return create_reply(result, msg)
        else:
            pass
    else:
        return create_reply('指令不清晰，请重新输入', msg)
