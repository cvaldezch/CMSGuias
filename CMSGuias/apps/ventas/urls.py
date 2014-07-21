#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import *


# Urls Projects
project_urls = patterns('',
    url(r'^$',ProjectsList.as_view(), name='view_projects'),
    url(r'^manager/(?P<project>\w+)/$', ProjectManager.as_view(), name='managerpro_view'),
)

urlpatterns = patterns('',
    # url to home
    url(r'^$', SalesHome.as_view(), name='view_sale'),
    url(r'^projects/', include(project_urls)),
)