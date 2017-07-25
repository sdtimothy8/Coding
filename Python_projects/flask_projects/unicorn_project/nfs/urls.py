from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'wangyaoli@inspur.com'

urlpatterns = [
    url(r'^$', views.nfs.as_view()),
    url(r'^checknfs/$', views.checknfs.as_view()),
    url(r'^uid/$', views.checkuid.as_view()),
    url(r'^gid/$', views.checkgid.as_view()),
    url(r'^dir/$', views.checkdir.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
