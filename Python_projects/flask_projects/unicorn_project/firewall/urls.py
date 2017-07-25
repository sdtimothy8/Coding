"""
This is the route module for firewall related functions.
"""
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'shaomingwu@inspur.com'

urlpatterns = [
    # Examples:
    url(r'^$', views.FirewallList.as_view()),
    url(r'^move/$', views.FirewallMove.as_view()),
    url(r'^(?P<itemid>[\w-]+)/$', views.FirewallDetail.as_view()),
    url(r'^firewalld/status/$', views.FirewallStatusList.as_view()),
    url(r'^firewalld/reload/$', views.FirewallReload.as_view()),
    url(r'^firewalld/config_type/$', views.FirewallConfigType.as_view()),
    # url(r'^firewalld/icmp/$', views.FirewallICMP.as_view()),
    url(r'^firewalld/panic/$', views.FirewalldPnaicMode.as_view()),
    url(r'^firewalld/zones/$', views.FirewallZoneList.as_view()),
    url(r'^firewalld/active_zones/$', views.FirewallActiveZones.as_view()),
    url(r'^firewalld/default_zone/$', views.FirewallDefaultZones.as_view()),
    url(r'^firewalld/services/$', views.FirewallService.as_view()),
    url(r'^firewalld/enable_services/$', views.FirewallEnableService.as_view()),
    url(r'^firewalld/ports/$', views.FirewallPorts.as_view()),
    url(r'^firewalld/interfaces/$', views.FirewallInterface.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
