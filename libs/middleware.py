import json
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

from libs.jwt_handler import custom_rest_exception_format


class ProcessExceptionMiddleware(MiddlewareMixin):
    """
    Django 中间件
    """

    def process_request(self, request):
        """
        去掉csrf检查
        :param request:
        :return:
        """
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_response(self, request, response):
        """
        :param request:
        :param response:
        :return:
        """
        if response:
            # noinspection PyBroadException
            try:
                data = response.data
                # logging.warning('处理异常信息：{0} {1}'.format(datetime.datetime.now(), data))
                if data is None:
                    return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")
                else:
                    pass
                if response.status_code == 400:
                    msg = custom_rest_exception_format(response).data
                    print(response.data)
                    return HttpResponse(json.dumps(msg), status=response.status_code, content_type="application/json")
            except:
                pass
                # logging.warning('{0} ProcessExceptionMiddleware process_response 异常'.format(datetime.now()))
        return response
