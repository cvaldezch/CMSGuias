#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    # url to home
    url(r'^$', SalesHome.as_view(), name='view_sale'),
    url(r'^projects/$',ProjectsList.as_view(), name='view_projects'),
)