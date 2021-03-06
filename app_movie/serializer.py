import re

from django.db.models import Q
from rest_framework import serializers

from app_movie.models import DoubanMovieSimple, DoubanMovie, MovieResource, MovieImage, UserMovieSimpleMark
from app_user.serializer import UserSimpleSerializer


class DoubanMovieSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubanMovieSimple
        fields = ('id', 'douban_id', 'title', 'cover', 'cover_x', 'cover_y', 'is_new', 'rate', 'url', 'douban_tag', 'douban_type', 'level', 'resources')


class DoubanMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubanMovie
        fields = ('id', 'douban_id', 'json_data', 'show_times', 'select_times')


class MovieResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieResource
        fields = ('id', 'title', 'name', 'source', 'download_link', 'show_times', 'like_times', 'dislike_times', 'report_times')


class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieImage
        fields = ('source', 'created_time', 'updated_time')


class UserMovieSimpleMarkSerializer(serializers.ModelSerializer):
    user_obj = serializers.SerializerMethodField()

    class Meta:
        model = UserMovieSimpleMark
        fields = '__all__'

    def get_user_obj(self, obj):
        if isinstance(obj, UserMovieSimpleMark):
            serializer = UserSimpleSerializer(obj.user)
        else:
            serializer = UserSimpleSerializer(obj['user'])
        return serializer.data


class UserMovieSimpleMarkDetailSerializer(serializers.ModelSerializer):
    movie_simple_detail = serializers.SerializerMethodField()

    class Meta:
        model = UserMovieSimpleMark
        fields = '__all__'

    def get_movie_simple_detail(self, obj):
        return DoubanMovieSimpleSerializer(obj.movie_simple).data
