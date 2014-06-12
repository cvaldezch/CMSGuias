# -*- coding: utf-8 -*-
#from django.conf.urls.defaults import patterns, url
from django.conf.urls import patterns, url
import views


urlpatterns = patterns('CMSGuias.apps.almacen.views',

    url(r'^$', views.StorageHome.as_view(), name='vista_storage'),
    # orders
    url(r'^pedido/generate/$','view_pedido',name='vista_pedido'),
    url(r'^orders/pending/$','view_orders_pending',name='vista_slope_orders'),
    url(r'^list/oreders/approved/$','view_orders_list_approved',name='vista_list_approved'),
    url(r'^meet/order/(?P<oid>.*)/$','view_attend_order',name='vista_meet_order'),
    # guide remisions
    url(r'^list/orders/meet/out/$','view_generate_guide_orders',name='vita_list_orders_outmeet'),
    url(r'^generate/(?P<oid>.*)/document/out/$','view_generate_document_out',name='vista_outdocument'),
    url(r'^list/guide/referral/$','view_list_guide_referral_success',name='vista_lista_guide_success'),
    url(r'^list/guide/referral/canceled/$','view_list_guide_referral_canceled',name='vista_lista_guide_canceled'),
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
    # carrier
    url(r'^upkeep/carrier/$','view_carrier',name='vista_carrier'),
    url(r'^upkeep/carrier/add/$','view_carrier_add',name='vista_carrier_add'),
    url(r'^upkeep/carrier/edit/(?P<ruc>.*)/$','view_carrier_edit',name='vista_carrier_edit'),
    # Transport
    url(r'^upkeep/transport/add/(?P<tid>.*)/$','view_transport_add', name='vista_transport_add'),
    url(r'^upkeep/transport/edit/(?P<cid>.*)/(?P<tid>.*)/$','view_transport_edit', name='vista_transport_edit'),
    url(r'^upkeep/transport/(?P<ruc>.*)/$','view_transport', name='vista_transport'),
    # Conductor
    url(r'^upkeep/conductor/add/(?P<tid>.*)/$','view_conductor_add', name='vista_conductor_add'),
    url(r'^upkeep/conductor/edit/(?P<cid>.*)/(?P<tid>.*)/$','view_conductor_edit', name='vista_conductor_edit'),
    url(r'^upkeep/conductor/(?P<ruc>.*)/$','view_conductor', name='vista_conductor'),
    # urls module storage
    url(r'^inventory/$', views.InventoryView.as_view(), name='vista_inventory'),
    url(r'^supply/$', views.SupplyView.as_view(), name='vista_supply'),
    url(r'^summary/list/orders/$', views.ListOrdersSummary.as_view(), name='vista_summary_orders'),
    url(r'^orders/details/supply/$', views.ListDetOrders.as_view(), name='vista_orders_details'),
)