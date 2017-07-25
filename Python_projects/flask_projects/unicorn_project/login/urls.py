from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Login.as_view(), name='login'),
    url(r'^off/$', views.Logoff.as_view(), name='logoff'),
]
