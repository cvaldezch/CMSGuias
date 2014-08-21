# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from views import *


urlpatterns = patterns('',
    url(r'^$', SignUpSupplier.as_view(), name='view_supplier_signup'),
)