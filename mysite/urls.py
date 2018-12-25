from django.conf.urls import url
from mysite import views
from django.urls import path
from django.views.generic import TemplateView

# SET THE NAMESPACE!
app_name = 'mysite'

urlpatterns=[
    url(r'^[a-z]{0,10}/pagination/(?P<start>[0-9]{0,4})/$', views.scroll, name='scroll'),
    url(r'^$', views.homepage, name='homepage'),
    url(r'^clip$', views.clip, name='clip'),
    url(r'^clip/(?P<hash_title>\d+)/$', views.clip_post, name='clip_post'),
    url(r'^favorites$', views.favorites, name='favorites'),
    url(r'^filter/(?P<query>\w+)/$', views.filter_query, name='filter_query'),
    url(r'^filter/(?P<tags>[\-?\w+]*)/(?P<sources>[\-?\w+]+)$', views.filter, name='filter_total'),
    url(r'^filter/(?P<tags>[\-?\w+]*)/(?P<sources>[\-?\w+]+)/pagination/(?P<start>[0-9]{0,4})/$', views.scroll_filter, name='scroll_filter'),
    url(r'^login/\w*$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^registrator/$', views.register, name='registrator'),
    url(r'^search/(?P<query>[\w*\d*\s*]+)/$', views.search, name='search'),
    url(r'^search/(?P<query>[\w*\d*\s*]+)//pagination/(?P<start>\d+)$', views.search_pagination, name='search_pagination'),
]
