# coding=utf-8
"""
This is the main module for disk management.
"""
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'shaomingwu@inspur.com'


urlpatterns = [
    # Ethernets list related URI resource.
    url(r'^capacity/$', views.DiskMgr.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
