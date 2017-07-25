"""
This is the main router for ethernet related functions.
"""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'yuxiubj@inspur.com'


urlpatterns = [
    # log file list related URI resource.
    url(r'^$', views.LogList.as_view()),
    # One log item details.
    # url(r'^(?P<itemid>[.\w-]+)/$', views.LogDetail.as_view()),
    url(r'^(?P<itemid>[^\\\/]+)/$', views.LogDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
