from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'wangyaoli@inspur.com'

urlpatterns = [
    url(r'^sync/$', views.Synchronoustime.as_view()),
    url(r'^ssltime/$', views.ssltime.as_view()),
    url(r'^currenttime/$', views.currentTime.as_view()),
    url(r'^$', views.times.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
