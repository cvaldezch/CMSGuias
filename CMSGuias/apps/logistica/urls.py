# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.LogisticsHome.as_view(), name='view_logistics'),
    url(r'^supply/status/pending/$', views.SupplyPending.as_view(), name='view_supply_pending'),
    url(r'^supply/to/convert/',views.SupplytoDocumentIn.as_view(), name='view_convert_supply'),
    url(r'^quotation/list/$',views.ViewListQuotation.as_view(), name='view_quote_list'),
    url(r'^quote/single/$', views.ViewQuoteSingle.as_view(), name='view_quote_single'),
    url(r'^purchase/single/$', views.ViewPurchaseSingle.as_view(), name='view_purchase_single'),
)