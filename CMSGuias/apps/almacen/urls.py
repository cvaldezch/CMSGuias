from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('CMSGuias.apps.almacen.views',
	url(r'^pedido/generate/$','view_pedido',name='vista_pedido'),
	# customers
	url(r'^keep/customers/$','view_keep_customers',name='vista_customers'),
	url(r'^keep/customers/add/$','view_keep_add_customers',name='vista_add_customers'),
	url(r'^keep/customers/(?P<ruc>.*)/edit/$','view_keep_edit_customers',name='vista_edit_customers'),
	# projects
	url(r'^keep/project/$','view_keep_project',name='vista_project'),
	url(r'^keep/project/add/$','view_keep_add_project',name='vista_add_projects'),
	url(r'^keep/project/(?P<proid>.*)/edit/$','view_keep_edit_project',name='vista_edit_projects'),
	# subproyectos
	url(r'^keep/project/subproyectos/(?P<pid>.*)/$','view_keep_sub_project',name='vista_sub_project'),
	# url(r'^keep/project/subproyectos/add/$','view_keep_add_project',name='vista_add_sub_projects'),
	# url(r'^keep/project/subproyectos/(?P<proid>.*)/(?P<sid>.*)/edit/$','view_keep_edit_project',name='vista_edit_sub_projects'),
)