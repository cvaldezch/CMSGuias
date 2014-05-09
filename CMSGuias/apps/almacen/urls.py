from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('CMSGuias.apps.almacen.views',
	url(r'^pedido/generate/$','view_pedido',name='vista_pedido'),
	# customers
	url(r'^keep/customers/$','view_keep_customers',name='vista_customers'),
	url(r'^keep/customers/add/$','view_keep_add_customers',name='vista_add_customers'),
	url(r'^keep/customers/(?P<ruc>.*)/edit/$','view_keep_edit_customers',name='vista_edit_customers'),
	#projects
	url(r'^keep/project/$','view_keep_project',name='vista_project'),
	url(r'^keep/project/add/$','view_keep_add_project',name='vista_add_projects'),
	url(r'^keep/project/(?P<proid>.*)/edit/$','view_keep_edit_project',name='vista_edit_projects'),
)