# -*- coding: utf-8 -*-
# from django.conf.urls.defaults import patterns, url
from django.conf.urls import patterns, url, include

from .views import *

# urls recurrents
urls_crossdomain = patterns(
    '',
    url(r'^data/ruc/$', RestfulDataRuc.as_view()),
)
urls_brands = patterns(
    '',
    url(r'^list/option/$', SearchBrand.as_view()),
)
urls_models = patterns(
    '',
    url(r'^list/option/$', SearchModel.as_view()),
)
urls_conf = patterns(
    '',
    url(r'^igv/$', GetIVAYear.as_view()),
)
urlpatterns = patterns(
    'CMSGuias.apps.wsjson.views',
    # temp Orders
    url(r'^get/materials/code/$', GetDetailsMaterialesByCode.as_view()),
    url(r'^get/materials/name/$', 'get_description_materials'),
    url(r'^get/meter/materials/$', 'get_meter_materials'),
    url(r'^get/resumen/details/materiales/$', 'get_resumen_details_materiales'),
    url(r'^post/aggregate/tmp/materials/$', 'save_order_temp_materials'),
    url(r'^post/update/tmp/materials/$', 'update_order_temp_materials'),
    url(r'^post/delete/tmp/materials/$', 'delete_order_temp_material'),
    url(r'^post/delete/all/temp/order/$', 'delete_all_temp_order'),
    url(r'^get/list/temp/order/$', 'get_list_order_temp'),
    url(r'^post/upload/orders/temp/$', 'post_upload_file_temp_orders'),
    # temp Oreders Nipples
    url(r'^get/nipples/temp/oreder/$', 'get_list_beside_nipples_temp_orders'),
    url(r'^get/list/temp/nipples/$', 'get_list_temp_nipples'),
    url(r'^post/saved/temp/nipples/$', 'post_saved_update_temp_nipples'),
    url(r'^post/delete/temp/nipples/item/$', 'post_delete_temp_item_nipple'),
    url(r'^post/delete/all/temp/nipples/$', 'post_delete_temp_all_nipple'),
    # Orders
    url(r'^post/approved/orders/$', 'post_approved_orders'),
    url(r'^post/cancel/orders/$', 'post_cancel_orders'),
    # url recurrent
    url(r'^get/details/materials/$', 'get_details_materials_by_id'),
    url(r'^get/projects/list/$', 'get_list_projects'),
    url(r'^get/sectors/list/$', 'get_list_sectors'),
    url(r'^get/subprojects/list/$', 'get_list_subprojects'),
    url(r'^get/stores/list/$', 'get_list_stores'),
    url(r'^get/list/transport/(?P<truc>.*)/$', 'get_recover_list_transport'),
    url(r'^get/list/conductor/(?P<truc>.*)/$', 'get_recover_list_conductor'),
    url(r'^supplier/get/list/all/$', getSupplierList.as_view()),
    url(r'^store/get/list/all/$', getStoreList.as_view()),
    # recurrent country, departament, province, district
    url(r'^country/list/', ViewContry.as_view()),
    url(r'^departament/list/', ViewDepartament.as_view()),
    url(r'^province/list/', ViewProvince.as_view()),
    url(r'^district/list/', ViewDistrict.as_view()),
    # url get data sunat
    url(r'^sunat/exchange/rate/$', RestfulExchangeRate.as_view()),
    # Class Bases-View Genereics
    url(r'^get/list/orders/details/$', get_OrdersDetails.as_view()),
    url(r'^get/details/supply/(?P<sid>.*)/$', SupplyDetailView.as_view()),
    url(r'^brand/', include(urls_brands)),
    url(r'^model/', include(urls_models)),
    url(r'^projects/lists/$', ViewCopyMaterialesProjectsSale.as_view()),
    url(r'^get/path/$', TreePath.as_view()),
    url(r'^restful/', include(urls_crossdomain)),
    url(r'^general/conf/', include(urls_conf)),
    # convert number a literal
    url(r'^convert/number/to/literal/', GetNumberLiteral.as_view()),
    url(r'^get/group/materials/bedside/$', SearchGroupMaterials.as_view()),
    # get all emails for accounts
    url(r'^get/emails/$', SystemEmails.as_view()),
    url(r'^emails/$', SystemEmails.as_view()),
    url(r'^post/key/confirm/$', KeyConfirmMan.as_view()),
    # urls export data
    url(r'^export/data/sector/(?P<pro>\w{7})/(?P<sec>\w+)/',
        ExportMetProject.as_view()),
    url(r'^export/data/materials/db/', ExportMaterialsDB.as_view()),
    url(r'^get/emails/starts/$', EmailsForsProject.as_view()),
)
