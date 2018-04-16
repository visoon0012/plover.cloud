from rest_framework import serializers

from app_system.models import UserSSConfig
from app_user.serializer import UserSimpleSerializer


class UserSSConfigCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSSConfig
        fields = ('system_ip', 'system_name', 'system_pass', 'ss_port', 'ss_pass', 'is_share')


class UserSSConfigModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSSConfig
        fields = '__all__'


class UserSSConfigSerializer(serializers.ModelSerializer):
    user_obj = serializers.SerializerMethodField()

    class Meta:
        model = UserSSConfig
        fields = ('id', 'user', 'user_obj', 'system_ip', 'ss_port', 'ss_pass', 'is_share', 'error_times')

    def get_user_obj(self, obj):
        if isinstance(obj, UserSSConfig):
            serializer = UserSimpleSerializer(obj.user)
        else:
            serializer = UserSimpleSerializer(obj['user'])
        return serializer.data
