from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from . import cpu_num

__author__ = 'zhuysh@inspur.com'

urlpatterns = [
    # Resource list related URI resource.
    url(r'^$', views.ResourceList.as_view()),
    url(r'^pci/', views.ResourcePciList.as_view()),
    url(r'^usb/', views.ResourceUsbList.as_view()),
    url(r'^ps/$', views.PsList.as_view()),
    url(r'^psdetail/$', views.PsDetail.as_view()),
    url(r'^pscpumem/$', views.PsCpuMemInfo.as_view()),
    url(r'^psnetinfo/$', views.NetIOInfo.as_view()),
    url(r'^psdiskinfo/$', views.DiskIOInfo.as_view()),
    url(r'^nethistory/$', views.NetHistoryInfo.as_view()),
    url(r'^pslist/(?P<itemid>[.\w-]+)/$', views.PsListInfo.as_view()),
    url(r'^cpunum/$', cpu_num.CpuNumView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
