#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from . import eth_views

__author__ = 'liushaolin@inspur.com'

urlpatterns = [
    url(r'^$', views.DeviceList.as_view()),
    url(r'^(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/$', views.ConnectionDetail.as_view()),
    url(r'^add_conn/$', views.AddConnection.as_view()),
    url(r'^eth_names/$', eth_views.EthNameList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
