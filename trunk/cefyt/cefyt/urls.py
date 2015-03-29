from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^sia/', include('sia.urls', namespace="sia")),
    url(r'^admin/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/sia/cuenta'}),
    url(r'^admin/', include(admin.site.urls)),
)
