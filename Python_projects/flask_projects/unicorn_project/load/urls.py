from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'zhangyuanfang@inspur.com'

urlpatterns = [
    # service URI resource.
    url(r'^$', views.ServiceManage.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
