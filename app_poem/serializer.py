from rest_framework import serializers

from app_poem.models import Author, Dynasty, Tag, Poem


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'created_time', 'updated_time')


class DynastySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dynasty
        fields = ('id', 'name', 'created_time', 'updated_time')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_time', 'updated_time')


class PoemSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    dynasty = DynastySerializer()
    tags = TagSerializer()

    class Meta:
        model = Poem
        fields = ('id', 'title', 'content', 'author', 'dynasty', 'tags', 'created_time', 'updated_time')
