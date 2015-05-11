from django.conf.urls import patterns, url
from indexsite import views

urlpatterns = patterns('',
    url(r'^$', views.register, name='register'),
    url(r'^read/$', views.read, name='read'),
    url(r'^read/load/$', views.loadread, name='loadread'),
    url(r'^rsslist/$', views.rsslist, name='rsslist'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm, name='register_confirm'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^makeread/(?P<id>\d+)/$', views.makeread, name='makeread'),
)