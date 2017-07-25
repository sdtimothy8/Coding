from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'wangyaoli@inspur.com'

urlpatterns = [
    url(r'^$', views.group.as_view()),
    url(r'^(?P<gname>[\w-]+)/$', views.groupdetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
