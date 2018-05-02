"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from app_book.views import NovelViewset, NovelChapterViewset, NovelForkViewset
from app_message.views import SystemMessageViewset
from app_movie.views import MovieSimpleViewset, MovieResourceViewset, MovieViewset, UserMovieSimpleMarkViewset
from app_system.views import UserSSConfigViewset
from app_user.views import UserViewset
from app_wechat.views import wechat
from config.settings import STATIC_ROOT, MEDIA_ROOT

from rest_framework import routers
from app_poem.views import PoemViewset
from config.swagger_schema import SwaggerSchemaView

router = routers.DefaultRouter()

#
router.register(r'poem', PoemViewset)
#
router.register(r'novel', NovelViewset)
router.register(r'novel_chapter', NovelChapterViewset)
router.register(r'novel_fork', NovelForkViewset)
#
router.register(r'movie_simple', MovieSimpleViewset)
router.register(r'movie_simple_mark', UserMovieSimpleMarkViewset)
router.register(r'movie_resource', MovieResourceViewset)
router.register(r'movie', MovieViewset)
#
router.register(r'system_message', SystemMessageViewset)
#
router.register(r'user', UserViewset)
#
router.register(r'system_ss', UserSSConfigViewset)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/spider/', include('app_spider.urls_api')),
    # JWT Auth
    url(r'^api/token/auth/', obtain_jwt_token),
    url(r'^api/token/refresh/', refresh_jwt_token),
    url(r'^api/token/verify/', verify_jwt_token),
    # DOCS
    url(r'^docs/', SwaggerSchemaView.as_view(), name="docs"),
    url(r'^wechat/', wechat, name='wechat'),
    #     url(r'^', include('app_web.urls')),
    #     url(r'^user/', include('app_user.urls')),
    #     url(r'^blog/', include('app_blog.urls')),
    #     # url(r'^movie/', include('app_movie.urls')),
    #     url(r'^message/', include('app_message.urls')),
    #     # API
    #     url(r'^api/image/', include('app_image.urls_api')),
    #     url(r'^api/book/', include('app_book.urls_api')),
    #     # url(r'^api/movie/', include('app_movie.urls_api')),
    #     url(r'^api/message/', include('app_message.urls_api')),
    #     # url(r'^api/user/', include('app_user.urls_api')),
]
urlpatterns += static('/static/', document_root=STATIC_ROOT)
urlpatterns += static('/media/', document_root=MEDIA_ROOT)
