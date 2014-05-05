from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('CMSGuias.apps.almacen.views',
	url(r'^pedido/generate/$','view_pedido',name='vista_pedido'),
)