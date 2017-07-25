from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

__author__ = 'zhuysh@inspur.com'

urlpatterns = [
    # faults manager URI.
    url(r'^events/(?P<itemid>[.\w-]+)/$', views.EventList.as_view()),
    url(r'^eventsdetail/(?P<itemid>[.\w-]+)/$', views.EventDetailList.as_view()),
    url(r'^faultsm/(?P<itemid>[.\w-]+)/$', views.FaultsManager.as_view()),
    url(r'^fmtype/(?P<itemid>[.\w-]+)/(?P<otype>[.\w-]+)/$', views.FmsManagerType.as_view()),
    url(r'^fmscmd/(?P<itemid>[.\w-]+)/$', views.FmscmdManager.as_view()),
    url(r'^monitor/$', views.FaultsMonitor.as_view()),
    url(r'^devcount/(?P<itemid>[.\w-]+)/$', views.DevCount.as_view()),
    url(r'^faultdetail/(?P<itemid>[.\w-]+)/$', views.FaultDetail.as_view()),
    url(r'^faultshow/(?P<itemid>[.\w-]+)/$', views.FaultShow.as_view()),
    url(r'^health/(?P<itemid>[.\w-]+)/$', views.FaultHealth.as_view()),
    url(r'^email/(?P<itemid>[.\S]+)/$', views.EmailSetting.as_view()),
    url(r'^ha/(?P<itemid>[.\w-]+)/$', views.HaSetting.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
