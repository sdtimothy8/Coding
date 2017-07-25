from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'caofengbing@inspur.com'

urlpatterns = [
    # Resource list related URI resource.

    url(r'^cpu/(?P<itemid>[.\w-]+)/$', views.CpuList.as_view()),
    url(r'^process/$', views.ProcessList.as_view()),
    url(r'^pslifecycle/$', views.ProcessLifeCycleList.as_view()),
    url(r'^psio/$', views.ProcessIOList.as_view()),
    url(r'^threads/$', views.ProcessThreadsList.as_view()),
    url(r'^files/$', views.ProcessFileList.as_view()),
    url(r'^fs/(?P<itemid>[.\w-]+)/$', views.FileSystemList.as_view()),
    url(r'^disk/(?P<itemid>[.\w-]+)/$', views.DiskList.as_view()),
    url(r'^mem/$', views.MemBasicInfo.as_view()),
    url(r'^swap/$', views.MemSwapInfo.as_view()),
    url(r'^page/$', views.PageInfo.as_view()),
    url(r'^slab/$', views.SlabInfo.as_view()),
    url(r'^numastat/$', views.NumastatInfo.as_view()),
    url(r'^throughput/$', views.ThroughputInfo.as_view()),
    url(r'^socket/$', views.SocketInfo.as_view()),
    url(r'^iptrafic/$', views.IptraficInfo.as_view()),
    url(r'^tcp/$', views.TCPInfo.as_view()),
    url(r'^udp/$', views.UDPInfo.as_view()),
    url(r'^memhistory/$', views.MemHistoryInfo.as_view()),
    url(r'^cpuhistory/$', views.CpuHistoryInfo.as_view()),
    url(r'^diskhistory/$', views.DiskHistoryInfo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
