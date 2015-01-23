from django.conf.urls import patterns, url

from sia import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^cuenta/$', views.cuenta, name='cuenta'),
    url(r'^registro/$', views.registro, name='registro'),
    #url(r'^crear_registro/$', views.crear_registro, name='crear_registro'),
)   