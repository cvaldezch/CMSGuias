# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from views import *


urlpatterns = patterns('',
    url(r'^signup/$', SignUpSupplier.as_view(), name='view_supplier_signup'),
    url(r'^logout/$', SignOutSupplier.as_view(), name='view_supplier_logout'),
    url(r'^$', SupplierHome.as_view(), name='supplier_home'),
    url(r'^quote/$', ListQuote.as_view(), name='supplier_quote'),
    url(r'quote/details/(?P<quote>\w{10})/(?P<supplier>\w{11})/$', ListDetailsQuote.as_view(), name='supplier_quote_details'),
    url(r'^purchase/$', ListOrderPurchase.as_view(), name='supplier_purchase'),
)