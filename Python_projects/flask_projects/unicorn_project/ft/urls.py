"""
This is the main router for ethernet related functions.
"""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'zhangguolei@inspur.com'


urlpatterns = [
    # filetrans list related URI resource.
    url(r'^$', views.FTList.as_view()),
    # One file item details.
    # url(r'^(?P<itemid>[.\w-]+)/$', views.FTDetail.as_view()),
    url(r'^(?P<itemid>[^\\\/]+)/$', views.FTDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
