from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_jwt import authentication

from app_message.models import SystemMessage, UserMessage
from app_message.serializer import SystemMessageSerializer, UserMessageSerializer
from libs.permissions import IsReadOnlyOrAdmin, UserMessagePermission


class SystemMessageViewset(viewsets.ModelViewSet):
    permission_classes = (IsReadOnlyOrAdmin,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = SystemMessage.objects.get_queryset().order_by('-id')
    serializer_class = SystemMessageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('title',)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'error': '您没有此权限'}, 400)
        else:
            super().create(self, request, *args, **kwargs)


class UserMessageViewset(viewsets.ModelViewSet):
    permission_classes = (UserMessagePermission,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = UserMessage.objects.get_queryset().order_by('-id')
    serializer_class = UserMessageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('title',)
