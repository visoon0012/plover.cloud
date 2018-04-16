from rest_framework import serializers

from app_book.models import Novel, NovelFork, NovelChapter


class NovelSerializer(serializers.ModelSerializer):
    forks = serializers.SerializerMethodField()
    new = serializers.SerializerMethodField()

    class Meta:
        model = Novel
        fields = ('id', 'title', 'intro', 'author', 'cover', 'forks', 'new', 'link', 'like_times', 'dislike_times', 'error_times', 'created_time', 'updated_time')

    def get_forks(self, obj):
        nfs = NovelFork.objects.filter(novel_id=obj.id, used=True)
        return len(nfs)

    def get_new(self, obj):
        nc = NovelChapter.objects.filter(novel_id=obj.id).last()
        return NovelChapterSerializer(nc).data


class NovelChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NovelChapter
        fields = '__all__'


class NovelForkSerializer(serializers.ModelSerializer):
    novel = NovelSerializer()
    read = NovelChapterSerializer()

    class Meta:
        model = NovelFork
        fields = ('id', 'user', 'novel', 'read', 'used', 'created_time', 'updated_time')
