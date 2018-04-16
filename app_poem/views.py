from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app_poem.models import Poem
from app_poem.serializer import PoemSerializer


class PoemViewset(viewsets.ModelViewSet):
    """
    the viewset let us can get data from api url
    like:curl - H 'application/json;indent=4' http://localhost:8080/api/articles/
    of course,we can get some author's article through:
    http://localhost:8080/api/articles/?author=2(author's id)
    Generally,people like to see json data,so when visit by browser,you should add
    ?format=json ,that is,http://localhost:8080/api/articles/?format=json

    """
    permission_classes = (AllowAny,)
    queryset = Poem.objects.get_queryset().order_by('id')
    serializer_class = PoemSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('id', 'title', 'content', 'author__name', 'dynasty__name', 'tags__name')
    search_fields = ('title', 'content', 'author__name', 'dynasty__name', 'tags__name')

    @list_route(url_path='random')
    def random(self, request):
        """随机获取"""
        result = {
            'count': 5,
            'next': '',
            'previous': '',
            'results': []
        }
        poems = Poem.objects.order_by('?')[:5]
        for poem in poems:
            serializer = PoemSerializer(poem)
            result['results'].append(serializer.data)
        return Response(result)
