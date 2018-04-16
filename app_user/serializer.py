from rest_framework import serializers

from app_user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'introduction', 'phone', 'is_staff', 'is_active', 'score', 'like_times', 'dislike_times', 'report_times')
        read_only_fields = ('is_staff', 'is_active', 'score', 'like_times', 'dislike_times', 'report_times')


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname',)
        read_only_fields = ('id', 'username', 'nickname',)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'password')

    def create(self, data):
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user


class UserForgotSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, data):
        try:
            user = User.objects.get(username=data['username'], email=data['email'])
            user.set_password(data['password'])
            user.save()
        except Exception as e:
            raise serializers.ValidationError('没有对应的用户，请检查您的用户名或邮箱')
        return user

    def update(self, instance, validated_data):
        pass
