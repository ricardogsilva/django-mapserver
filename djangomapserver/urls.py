from django.conf.urls import patterns, url
import views

# TODO - Add WFS and WCS endpoints
urlpatterns = patterns('',
    url(r'^wms$', views.wms_endpoint, name='wms_endpoint')
)
