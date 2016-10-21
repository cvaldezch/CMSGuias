# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from views import *

urlcrud = patterns('',
    url(r'^create/supplier/$', SupplierCreate.as_view(), name='view_create_supplier'),
)

urlpatterns = patterns('',
    url(r'^$', LogisticsHome.as_view(), name='view_logistics'),
    url(r'^supply/status/pending/$', SupplyPending.as_view(), 
        name='view_supply_pending'),
    url(r'^supply/to/convert/', SupplytoDocumentIn.as_view(), 
        name='view_convert_supply'),
    url(r'^quotation/list/$', ViewListQuotation.as_view(), 
        name='view_quote_list'),
    url(r'^quote/single/$', ViewQuoteSingle.as_view(), 
        name='view_quote_single'),
    url(r'^purchase/single/$', ViewPurchaseSingle.as_view(), 
        name='view_purchase_single'),
    url(r'^purchase/list/$', ListPurchase.as_view(), 
        name='view_purchase_list'),
    url(r'^supplier/login/$', LoginSupplier.as_view(), 
        name='view_login_suppler'),
    url(r'^compare/quote/(?P<quote>\w+)/', CompareQuote.as_view(), 
        name='view_compare_quote'),
    url(r'^ingress/price/supplier/(?P<quote>\w{10})/(?P<supplier>\w{11})/',
        IngressPriceQuote.as_view(), name='view_ingress_price_supplier'),
    url(r'^crud/', include(urlcrud)),
    url(r'^materials/(?P<pro>\w{7})/compressed/$', ListCompressed.as_view(), 
        name='compressed_list'),
    url(r'^services/orders/$', ServiceOrders.as_view(), 
        name='orders_service'),
    url(r'^price/materials/$', PriceMaterialsViews.as_view(), 
        name='materials_price_views'),
    url(r'^consult/purchase/$', ConsultPurchase.as_view(), 
        name='consult_purchase_view'),
    url(r'^services/orders/(?P<oservice>\w{10})/$', 
        EditServiceOrder.as_view(), name='edorderservice_view'),
)
