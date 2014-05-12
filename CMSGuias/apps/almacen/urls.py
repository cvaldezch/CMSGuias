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
	url(r'^keep/subproyectos/add/(?P<pid>.*)/$','view_keep_add_subproyeto',name='vista_add_sub_projects'),
	url(r'^keep/subproyectos/edit/(?P<pid>.*)/(?P<sid>.*)/$','view_keep_edit_subproyecto',name='vista_edit_sub_projects'),
	url(r'^keep/subproyectos/(?P<pid>.*)/$','view_keep_sub_project',name='vista_sub_project'),
	# sectores
	url(r'^keep/sectores/edit/(?P<pid>.*)/(?P<sid>.*)/(?P<cid>.*)/$','view_keep_edit_sector',name='vista_edit_sector'),
	url(r'^keep/sectores/add/(?P<proid>.*)/(?P<sid>.*)/$','view_keep_add_sector',name='vista_add_sectors'),
	url(r'^keep/sectores/(?P<pid>.*)/(?P<sid>.*)/$','view_keep_sec_project',name='vista_sec_project'),
	# Almacenes
	url(r'^upkeep/stores/$','view_stores',name='vista_stores'),
	url(r'^upkeep/stores/add/$','view_stores_add',name='vista_stores_add'),
	url(r'^upkeep/stores/edit/(?P<aid>.*)/$','view_stores_edit',name='vista_stores_edit'),
)