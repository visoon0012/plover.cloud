import json
import re
from io import BytesIO

import requests
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins, status
from rest_framework.decorators import list_route, action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_jwt import authentication

from app_movie import utils
from app_movie.models import DoubanMovieSimple, DoubanMovie, MovieResource, MovieImage, UserMovieSimpleMark
from app_movie.serializer import DoubanMovieSimpleSerializer, DoubanMovieSerializer, MovieResourceSerializer, UserMovieSimpleMarkSerializer
from libs.permissions import IsReadOnlyOrAdmin, IsOwnerOrReadOnly
from libs.spider.movie_spider import douban_spider


class MovieSimpleViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsReadOnlyOrAdmin,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = DoubanMovieSimple.objects.get_queryset().order_by('-level')
    serializer_class = DoubanMovieSimpleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', 'douban_id', 'title', 'douban_tag', 'douban_type',)
    search_fields = ('title',)

    @action(methods=['GET'], detail=False)
    def status(self, request):
        return Response({'status': True, 'status2': False})

    @action(methods=['GET'], detail=False)
    def auto(self, request):
        utils.auto_get_movie_detail()
        return Response({'message': 'ok'})

    @list_route()
    def spider(self, request):
        """
        description: 电影简介爬虫 - 从豆瓣电影取数据
        parameters:
          - name: tag
            type: string
            required: true
            location: query
            description: 热门/
          - name: type
            type: string
            required: true
            location: query
            description: movie / tv
        """
        m_type = request.GET.get('type', 'movie')
        m_tag = request.GET.get('tag', '热门')
        return utils.get_movie_simple(m_type, m_tag)

    @list_route(methods=['post'])
    def image(self, request):
        url = request.data['url']
        movie_image, created = MovieImage.objects.get_or_create(source=url)
        if not movie_image.is_used:
            try:
                response = requests.request("GET", url)
                image = Image.open(BytesIO(response.content))
                save_path = './media/movie_images/%s.png' % movie_image.id
                image.save(save_path)
                movie_image.is_used = True
                movie_image.save()
                return Response({'image_url': save_path})
            except Exception as e:
                print(e)
                return Response({'message': 'none data'}, status=400)
        else:
            save_path = './media/movie_images/%s.png' % movie_image.id
            return Response({'image_url': save_path})


class MovieViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsReadOnlyOrAdmin,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = DoubanMovie.objects.get_queryset().order_by('id')
    serializer_class = DoubanMovieSerializer

    @action(detail=False, methods=['GET'], url_name='detail', url_path='detail')
    def movie_detail(self, request):
        """
        description: 根据豆瓣id获取影片信息，如果数据库没有则去豆瓣搜索
        parameters:
          - name: douban_id
            type: string
            required: true
            location: query
            description: douban_id
        """
        douban_id = request.GET.get('douban_id', '')
        try:
            # 数据库存在该id记录
            douban_movie = DoubanMovie.objects.get(douban_id=douban_id)
            result = json.loads(douban_movie.json_data)
            # 更新字段的显示次数
            douban_movie.show_times += 1
            douban_movie.save()
        except ObjectDoesNotExist as e:
            print('新豆瓣影片信息')
            # 不存在该资源，到豆瓣查询
            result = douban_spider.search_detail(douban_id)
            # 保存到数据库
            DoubanMovie.objects.create(douban_id=douban_id, json_data=result).save()
            # 返回结果
            result = json.loads(result)
        return Response(result)


class MovieResourceViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsReadOnlyOrAdmin,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = MovieResource.objects.get_queryset().order_by('-id')
    serializer_class = MovieResourceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('id', 'title', 'name', 'source',)
    search_fields = ('title', 'name', 'source', 'download_link')

    @list_route()
    def search(self, request):
        result = []
        keywords = request.GET.get('keywords', '')
        if keywords == '':
            return Response({'message': '请输入关键字'}, 400)
        # 查询是否有该标题的下载资源
        keywords = re.split("[ !！?？.。：:()（）]", keywords)
        movie_resources = MovieResource.objects
        for keyword in keywords:
            movie_resources = movie_resources.filter(Q(name__icontains=keyword) | Q(title__icontains=keyword))
        sources = movie_resources.values('source').annotate(source_count=Count('source'))

        for source in sources:
            items = movie_resources.filter(source=source['source'])
            tmp_list = []
            for item in items:
                serializer = MovieResourceSerializer(item).data
                tmp_list.append(serializer)
            result.append(tmp_list)
        return Response(result)

    # @action(detail=False)
    # def search2(self, request):
    #     keywords = request.GET.get('keywords', '')
    #     if keywords == '':
    #         return Response({'message': '请输入关键字'}, 400)
    #     # 查询是否有该标题的下载资源
    #     keywords = re.split("[ !！?？.。：:()（）]", keywords)
    #     movie_resources = MovieResource.objects
    #     for keyword in keywords:
    #         movie_resources = movie_resources.filter(Q(name__icontains=keyword) | Q(title__icontains=keyword))
    #     df = pd.DataFrame(list(movie_resources.values()))
    #     df = df.fillna('unknow')
    #     result = df.groupby('source').apply(lambda g: g.to_dict('records')).to_dict()
    #     return Response(result)


class UserMovieSimpleMarkViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    queryset = UserMovieSimpleMark.objects.get_queryset().order_by('-id')
    serializer_class = UserMovieSimpleMarkSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user__id', 'movie_simple__douban_id',)

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response({'error': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        data['user'] = request.user.id
        if 'id' not in request.data.keys():
            serializer = UserMovieSimpleMarkSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            partial = kwargs.pop('partial', False)
            instance = UserMovieSimpleMark.objects.get(id=request.data['id'])
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
