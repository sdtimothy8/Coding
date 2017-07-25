# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#

from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'shanchaobj@inspur.com'

urlpatterns = [
    url(r'^vms/', views.VMList.as_view()),
    url(r'^vm/', views.VM.as_view()),
    url(r'^creator/', views.Creator.as_view()),
    url(r'^lifecycle/', views.Lifecycle.as_view()),
    url(r'^remove/', views.Remove.as_view()),
    url(r'^ip/', views.Ip.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
