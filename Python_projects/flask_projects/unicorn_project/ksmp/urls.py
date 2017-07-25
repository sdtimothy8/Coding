"""
This is the main module for router features for unicorn.
"""
from django.conf.urls import include, url
from django.contrib import admin

__author__ = 'shaomingwu@inspur.com'


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^diskmgr/', include('diskmgr.urls')),
    url(r'^firewall/', include('firewall.urls')),
    url(r'^fts/', include('ft.urls')),
    url(r'^logs/', include('log.urls')),
    url(r'^resources/', include('resources.urls')),
    url(r'^precmd/', include('precmd.urls')),
    url(r'^host/', include('host.urls')),
    url(r'^service/', include('load.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^group/', include('users.urls_group')),
    url(r'^tcp/', include('tcp.urls')),
    url(r'^packages/', include('packages.urls')),
    url(r'^times/', include('times.urls')),
    url(r'^index/', include('index.urls')),
    url(r'^login/', include('login.urls')),
    url(r'^monitor/', include('sysmonitor.urls')),
    url(r'^fans/', include('fans.urls')),
    url(r'^nfs/', include('nfs.urls')),
    url(r'^ftp/', include('ftp.urls')),
    url(r'^network/', include('network.urls')),
    url(r'^driver/', include('driverlist.urls')),
    url(r'^logmanager/', include('logmanager.urls')),
    url(r'^faultmanager/', include('faultmanager.urls')),
    url(r'^vmmanager/', include('vmmanager.urls')),
]
