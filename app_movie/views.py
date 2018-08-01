import datetime
import json
import re
from io import BytesIO

import requests
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_jwt import authentication

from app_movie import utils
from app_movie.models import DoubanMovieSimple, DoubanMovie, MovieResource, MovieImage, UserMovieSimpleMark
from app_movie.serializer import DoubanMovieSimpleSerializer, DoubanMovieSerializer, MovieResourceSerializer, UserMovieSimpleMarkSerializer, \
    UserMovieSimpleMarkDetailSerializer
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
        return Response({'status': True, 'status2': True})

    @action(methods=['GET'], detail=False)
    def auto_resources(self, request):
        """
        循环计算每个资源数，统计 todo
        :param request:
        :return:
        """
        count = 1
        for obj in self.queryset:
            count += 1
            keywords = re.split("[ !！?？.。：:()（）・·]", obj.title)
            movie_resources = MovieResource.objects.values('id')
            for keyword in keywords:
                movie_resources = movie_resources.filter(Q(name__icontains=keyword) | Q(title__icontains=keyword))
            if obj.douban_type == 'movie':
                movie_resources = movie_resources.exclude(name__iregex='连载至[0-9]+')
                movie_resources = movie_resources.exclude(name__iregex='[\u4e00-\u9fa5]*{}[0-9]+'.format(obj.title))
                movie_resources = movie_resources.exclude(title__iregex='连载至[0-9]+')
                movie_resources = movie_resources.exclude(title__iregex='[\u4e00-\u9fa5]*{}[0-9]+'.format(obj.title))
            obj.resources = movie_resources.count()
            obj.save()
        return Response({'message': 'ok'})

    @action(methods=['GET'], detail=False)
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

    @action(methods=['POST'], detail=False)
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

    # @action(detail=False, methods=['GET'])
    # def word2vec(self, request):
    #     """
    #     电影详情 - 词向量
    #     :param request:
    #     :return:
    #     """
    #     doc2vector.doc_segment()
    #     doc2vector.train()
    #     return Response({}, status=status.HTTP_200_OK)
    #
    # @action(detail=False, methods=['GET'])
    # def similar(self, request):
    #     """
    #     相似程度
    #     :param request:
    #     :return:
    #     """
    #     douban_id_1 = request.GET.get('douban_id_1', '26721664')
    #     douban_id_2 = request.GET.get('douban_id_2', '26721664')
    #     movie_info_1 = json.loads(self.queryset.get(douban_id=douban_id_1).json_data)['title']
    #     movie_info_2 = json.loads(self.queryset.get(douban_id=douban_id_2).json_data)['title']
    #     doc2vector.test_model(movie_info_1, movie_info_2)
    #     return Response({}, status=status.HTTP_200_OK)

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
            # 如果信息太旧了，同步最新的信息回来
            if douban_movie.updated_time < timezone.now() - datetime.timedelta(days=30):
                # print('影片信息过旧')
                result = douban_spider.search_detail(douban_id)
                douban_movie.json_data = result
                douban_movie.save()
            # 更新字段的显示次数
            result = json.loads(douban_movie.json_data)
            douban_movie.show_times += 1
            douban_movie.save()
        except ObjectDoesNotExist as e:
            # print('新豆瓣影片信息')
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

    @action(detail=False, methods=['GET'], url_name='search', url_path='search')
    def search(self, request):
        result = []
        keywords = request.GET.get('keywords', '')
        if keywords == '':
            return Response({'message': '请输入关键字'}, 400)
        # 查询是否有该标题的下载资源
        keywords = re.split("[ !！?？.。：:()（）・·]", keywords)
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

    @action(detail=False)
    def search_list(self, request):
        keywords = request.GET.get('keywords', '')
        douban_type = request.GET.get('douban_type', 'movie')
        keywords = re.split("[ !！?？.。：:()（）・·]", keywords)
        movie_resources = MovieResource.objects.order_by('-id')
        for keyword in keywords:
            movie_resources = movie_resources.filter(Q(name__icontains=keyword) | Q(title__icontains=keyword))
        # if douban_type == 'movie':
        #     movie_resources = movie_resources.exclude(name__iregex='连载至[0-9]+')
        #     movie_resources = movie_resources.exclude(name__iregex='[\u4e00-\u9fa5]*{}[0-9]+'.format(keywords))
        #     movie_resources = movie_resources.exclude(title__iregex='连载至[0-9]+')
        #     movie_resources = movie_resources.exclude(title__iregex='[\u4e00-\u9fa5]*{}[0-9]+'.format(keywords))
        serializer = MovieResourceSerializer(movie_resources, many=True)
        return Response(serializer.data)

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
    filter_fields = ('user__id', 'movie_simple__douban_id', 'movie_simple__id', 'is_fork')

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

    def list(self, request, *args, **kwargs):
        self.serializer_class = UserMovieSimpleMarkDetailSerializer
        return super(UserMovieSimpleMarkViewset, self).list(request, *args, **kwargs)
