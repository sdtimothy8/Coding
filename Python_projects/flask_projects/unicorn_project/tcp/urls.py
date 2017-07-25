from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'zhuysh@inspur.com'

urlpatterns = [
    # Tcp list related URI tcp.
    url(r'^deny/', views.TcpDenyList.as_view()),
    url(r'^allow/', views.TcpAllowList.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
