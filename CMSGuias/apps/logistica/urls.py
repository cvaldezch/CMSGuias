# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from views import *

urlcrud = patterns('',
    url(),
)

urlpatterns = patterns('',
    url(r'^$', LogisticsHome.as_view(), name='view_logistics'),
    url(r'^supply/status/pending/$', SupplyPending.as_view(), name='view_supply_pending'),
    url(r'^supply/to/convert/',SupplytoDocumentIn.as_view(), name='view_convert_supply'),
    url(r'^quotation/list/$',ViewListQuotation.as_view(), name='view_quote_list'),
    url(r'^quote/single/$', ViewQuoteSingle.as_view(), name='view_quote_single'),
    url(r'^purchase/single/$', ViewPurchaseSingle.as_view(), name='view_purchase_single'),
    url(r'purchase/list/$', ListPurchase.as_view(), name='view_purchase_list'),
    url(r'supplier/login/$', LoginProveedor.as_view(), name='view_login_suppler'),
)