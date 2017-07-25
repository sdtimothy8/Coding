from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'xiekun'

urlpatterns = [
    # Examples:
    url(r'^$', views.CmdList.as_view()),
    url(r'^(?P<cmdnum>\d+(,\d+)*)$', views.CmdDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
