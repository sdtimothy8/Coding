from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'caofengbing'

urlpatterns = [
    # Examples:
    url(r'^$', views.HostList.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
