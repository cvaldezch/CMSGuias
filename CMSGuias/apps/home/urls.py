#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls import patterns, url, include

from .views import *

customers_urls = patterns('',
    url(r'^list/$', CustomersList.as_view(), name='customers_list'),
    url(r'^new/$', CustomersCreate.as_view(), name='customers_new'),
    url(r'^edit/(?P<pk>\w+)/$', CustomersUpdate.as_view(), name='customers_edit'),
    url(r'^delete/(?P<pk>\w+)/$', CustomersDelete.as_view(), name='customers_del'),
)

urlpatterns = patterns('',
	url(r'^SignUp/$', LoginView.as_view(), name='vista_login'),
	url(r'^$', HomeManager.as_view(), name='vista_home'),
	url(r'^logout/$', LogoutView.as_view(), name='vista_logout'),
    url(r'^customers/', include(customers_urls)),
)