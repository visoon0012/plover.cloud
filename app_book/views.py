from time import sleep

from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_jwt import authentication

from app_book import spiders
from app_book.models import Novel, NovelChapter, NovelFork
from app_book.serializer import NovelSerializer, NovelChapterSerializer, NovelForkSerializer
from libs.permissions import IsOwnerOrReadOnly


class NovelViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = Novel.objects.get_queryset()
    serializer_class = NovelSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('title', 'author',)

    @list_route()
    def search(self, request):
        """
        按照书名到网上搜索小说 - (keywords - 书名)
        """
        keywords = request.GET.get('keywords', '')
        result = {
            'novel': None,
            'novel_chapters': None
        }
        try:
            novel_t = Novel.objects.get(title=keywords)
            result['novel'] = NovelSerializer(novel_t).data
            novel_chapters = NovelChapter.objects.filter(novel_id=novel_t.id)[0:10]
            result['novel_chapters'] = NovelChapterSerializer(novel_chapters, many=True).data
        except ObjectDoesNotExist as e:
            # 获取数据
            try:
                novel, novel_chapters = spiders.search_novel(keywords)
            except Exception as e:
                return Response({'error': '搜索不到此小说，请重试或换源'}, status.HTTP_400_BAD_REQUEST)
            # 存储数据
            novel_t = Novel.objects.create(title=novel['title'], author=novel['author'], cover=novel['cover'], intro=novel['intro'])
            novel_t.save()
            for novel_chapter in novel_chapters:
                print('缓存中: %s' % novel_chapter['title'])
                try:
                    # 已经存在了的小说章节
                    novel_chapter_obj = NovelChapter.objects.get(link=novel_chapter['link'])
                except ObjectDoesNotExist as e:
                    # 新的章节
                    NovelChapter.objects.create(novel=novel, title=novel_chapter['title'], link=novel_chapter['link']).save()
            result['novel'] = NovelSerializer(novel_t).data
            novel_chapters = NovelChapter.objects.filter(novel_id=novel_t.id)[0:10]
            result['novel_chapters'] = NovelChapterSerializer(novel_chapters, many=True).data
            print('新的小说')
        return Response(result)

    @list_route()
    def update_chapter(self, request):
        spiders.auto_update_fork()
        return Response({'success': '更新完毕'})


class NovelChapterViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = NovelChapter.objects.get_queryset()
    serializer_class = NovelChapterSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('title',)

    @detail_route()
    def chapters(self, request, *args, **kwargs):
        """
        小说的所有章节
        """
        novel_id = kwargs['pk']
        novel_chapters = NovelChapter.objects.filter(novel_id=novel_id)
        return Response(NovelChapterSerializer(novel_chapters, many=True).data)

    @list_route()
    def read(self, request):
        if request.user.is_anonymous:
            return Response({'token': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = request.user.id
        novel_id = request.GET.get('novel_id', '')
        read_id = request.GET.get('read_id', '')
        next_chapter = request.GET.get('next', 'false')
        last_chapter = request.GET.get('last', 'false')
        print(next_chapter)
        print(type(next_chapter))
        if read_id == 'undefined' or read_id == '0':
            chapter = NovelChapter.objects.filter(novel_id=novel_id).first()
        else:
            if next_chapter == 'true':
                chapter = NovelChapter.objects.filter(novel_id=novel_id).filter(id__gt=read_id).first()
            elif last_chapter == 'true':
                chapter = NovelChapter.objects.filter(novel_id=novel_id).filter(id__lt=read_id).last()
            else:
                chapter = NovelChapter.objects.get(id=read_id)
        if not chapter:
            return Response({'error': '没有对应的章节'}, status.HTTP_400_BAD_REQUEST)
        if len(chapter.content) == 0:
            chapter.content = spiders.search_novel_chapter(chapter.link)
            chapter.save()
        # 记录已读信息到数据库
        novel_fork = NovelFork.objects.get(user_id=user_id, novel_id=novel_id)
        novel_fork.read = chapter
        novel_fork.save()
        return Response(NovelChapterSerializer(chapter).data)

    @detail_route()
    def cache(self, request, *args, **kwargs):
        """
        缓存章节目录
        """
        if request.user.is_anonymous:
            return Response({'token': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)
        novel_id = kwargs['pk']
        novel = Novel.objects.get(id=novel_id)
        novel_t, novel_chapters = spiders.search_novel(novel.title)
        count = 0
        for novel_chapter in novel_chapters:
            print('缓存中: %s' % novel_chapter['title'])
            try:
                # 已经存在了的小说章节
                novel_chapter_obj = NovelChapter.objects.get(link=novel_chapter['link'])
            except ObjectDoesNotExist as e:
                # 新的章节
                count += 1
                NovelChapter.objects.create(novel=novel, title=novel_chapter['title'], link=novel_chapter['link']).save()
        return Response({'success': '缓存完毕，新增: %s' % count})

    @detail_route()
    def download(self, request, *args, **kwargs):
        """
        下载章节文本
        """
        if request.user.is_anonymous:
            return Response({'token': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)
        novel_id = kwargs['pk']
        novel_chapters = NovelChapter.objects.filter(novel_id=novel_id)
        count = 0
        for novel_chapter in novel_chapters:
            if len(novel_chapter.content) > 0:
                print('已有内容，跳过')
                continue
            try:
                sleep(3)
                count += 1
                content = spiders.search_novel_chapter(novel_chapter['link'])
                novel_chapter.content = content
                novel_chapter.save()
            except Exception as e:
                print(e)
        return Response({'success': '下载完毕，新增: %s' % count})

    @list_route()
    def auto_download(self):
        count = spiders.auto_download()
        return Response({'success': '下载完毕，新增: %s' % count})


class NovelForkViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = NovelFork.objects.get_queryset().filter(used=True)
    serializer_class = NovelForkSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user__id', 'novel__id')

    @detail_route(methods=['GET'])
    def fork(self, request, *args, **kwargs):
        """
        关注小说(id-小说id)
        """
        if request.user.is_anonymous:
            return Response({'token': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)
        novel_id = kwargs['pk']
        user_id = request.user.id
        try:
            try:
                novel_fork = NovelFork.objects.get(user_id=user_id, novel_id=novel_id)
                if novel_fork.used:
                    novel_fork.used = False
                    novel_fork.save()
                    return Response({'success': '您已经成功取消关注该小说'})
                else:
                    novel_fork.used = True
                    novel_fork.save()
                    return Response({'success': '您已经成功关注该小说'})
            except ObjectDoesNotExist as e:
                NovelFork.objects.create(user_id=user_id, novel_id=novel_id).save()
                return Response({'success': '已成功追加到您的小说库，并监控更新'})
        except Exception as e:
            return Response({'error': '不存在的小说，请先进行搜索'}, status.HTTP_400_BAD_REQUEST)
