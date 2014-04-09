from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('CMSGuias.apps.almacen.views',
	url(r'^$','view_home',name='vw_home'),
)