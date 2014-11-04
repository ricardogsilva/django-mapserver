from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^wms$', views.wms_endpoint, name='wms_endpoint')
)
