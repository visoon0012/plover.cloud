from rest_framework import viewsets, mixins, status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_jwt import authentication

from app_user.models import User
from app_user.serializer import UserSerializer, UserCreateSerializer, UserForgotSerializer
from libs.permissions import IsOwnerOrReadOnly


class UserViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(methods=['PUT'])
    def forgot(self, request, *args, **kwargs):
        serializer = UserForgotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
