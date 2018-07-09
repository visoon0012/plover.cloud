from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_jwt import authentication

from app_system import utils
from app_system.models import UserSSConfig
from app_system.serializer import UserSSConfigCreateSerializer, UserSSConfigSerializer, UserSSConfigModelSerializer
from libs.permissions import IsOwnerOrReadOnly


class UserSSConfigViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = UserSSConfig.objects.get_queryset().order_by('-id')
    serializer_class = UserSSConfigModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user__id',)

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response({'error': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSSConfigCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = UserSSConfig.objects.create(user=request.user, **serializer.data)
        instance.save()
        serializer = UserSSConfigModelSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(is_share=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSSConfigSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSSConfigSerializer(queryset, many=True)
        return Response(serializer.data)

    # @detail_route(methods=['GET'])
    # def config(self, request, *args, **kwargs):
    #     """
    #     配置服务器
    #     """
    #     instance = self.get_object()
    #     serializer = UserSSConfigCreateSerializer(instance)
    #     utils.config_ss(**serializer.data)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # @detail_route(methods=['GET'])
    # def restart(self, request, *args, **kwargs):
    #     """
    #     重启SS，传入UserSSConfig.id
    #     """
    #     instance = self.get_object()
    #     serializer = UserSSConfigCreateSerializer(instance)
    #     try:
    #         utils.reboot_ss(**serializer.data)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': '重启尚未完成，请稍后重试'}, status=status.HTTP_400_BAD_REQUEST)
    #
    # @list_route(methods=['GET'])
    # def user_servers(self, request, *args, **kwargs):
    #     """
    #     某个用户的SS服务器
    #     """
    #     if request.user.is_anonymous:
    #         return Response({'error': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)
    #     queryset = UserSSConfig.objects.filter(user=request.user).order_by('-id')
    #     serializer = UserSSConfigModelSerializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
