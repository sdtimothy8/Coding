from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'wangyaoli@inspur.com'

urlpatterns = [
    url(r'^disk/(?P<cmd>[a-z]+)/$', views.fdisklist.as_view()),
    url(r'^network/$', views.networklist.as_view()),
    url(r'^pci/$', views.pcilist.as_view()),
    url(r'^drivermodslist/$', views.drivermodslist.as_view()),
    url(r'^drivermodinfo/(?P<modname>[\w]+)/$', views.drivermodinfo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
