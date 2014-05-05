from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('CMSGuias.apps.wsjson.views',
	url(r'^get/materials/name/$','get_description_materials'),
	url(r'^get/meter/materials/$','get_meter_materials'),
	url(r'^get/resumen/details/materiales/$','get_resumen_details_materiales'),
	url(r'^post/aggregate/tmp/materials/$','save_order_temp_materials'),
	url(r'^post/update/tmp/materials/','update_order_temp_materials'),
	url(r'^get/list/temp/order/','get_list_order_temp'),
	# url recurrent
	url(r'^get/details/materials/$','get_details_materials_by_id'),
)