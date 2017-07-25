from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'zhangguolei@inspur.com'

urlpatterns = [
    # Resource list related URI resource.


    url(r'^unicorn/$', views.UnicornLog.as_view()),
    url(r'^kernel/$', views.KernelLog.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
