from django.conf.urls import patterns, url

from sia import views

urlpatterns = patterns(
    '',
    url(r'^$', views.cuenta, name='cuenta'),
    url(r'^cuenta/$', views.cuenta, name='cuenta'),
    url(r'^registro/$', views.registro, name='registro'),
    url(r'^generar_reporte/$', views.generar_reporte, name='generar_reporte'),
    url(r'^generar_cupon/$', views.generar_cupon, name='generar_cupon'),
    url(r'^listado_cuotas/$', views.listado_cuotas, name='listado_cuotas'),
    url(r'^procesar_pago/$', views.procesar_pago, name='procesar_pago'),
)
