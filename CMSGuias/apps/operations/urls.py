#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import *

urlpatterns = patterns('',
    # url to home
    url(r'^$', OperationsHome.as_view(), name='home_operations'),
    url(r'^list/preorders/(?P<pro>\w{7})/(?P<sub>\w+|)/(?P<sec>\w+)/$', ListPreOrders.as_view(), name='view_list_preordersop'),
)