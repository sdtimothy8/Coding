from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'wangyaoli@inspur.com'

urlpatterns = [
    url(r'^groups/(?P<url>.+(/.+)*)/$', views.packageslist.as_view()),
    url(r'^search/$', views.searchonepackage.as_view()),
    url(r'^$', views.packages.as_view()),
    url(r'^dir/$', views.filelist.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
