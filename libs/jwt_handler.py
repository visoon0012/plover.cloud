from datetime import datetime

from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler
from rest_framework_jwt.authentication import jwt_decode_handler

from app_user.serializer import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt返回
        def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


def rest_exception_handler(exc, context):
    """
    自定义reset错误返回格式
    :param exc:
    :param context:
    :return:
    """
    response = exception_handler(exc, context)  # 获取本来应该返回的exception的response
    if response is not None:
        response = custom_rest_exception_format(response)
    else:
        pass
    return response


def custom_rest_exception_format(response):
    # noinspection PyBroadException
    try:
        data = response.data
        # logging.warning('处理异常信息：{0} {1}'.format(datetime.datetime.now(), data))
        for key, item in data.items():
            if isinstance(item, list):
                # 如果是数组 取第一条信息
                first = item[0]
                if isinstance(first, str):
                    # 如果是字符串
                    value = first
                elif isinstance(first, dict):
                    # 如果是字典
                    fv = list(first.values())
                    value = fv[0]
                else:
                    # 其他格式
                    value = first
            elif isinstance(item, ErrorDetail):
                # 如果是错误详情
                value = item
            elif isinstance(item, str):
                # 如果是字符串
                value = item
            else:
                value = '未知的参数类型！'
            data[key] = value
        response.data = data
    except:
        logging.warning('{0} custom_rest_exception_format 异常'.format(datetime.now()))
    finally:
        return response
