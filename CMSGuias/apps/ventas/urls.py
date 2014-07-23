#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import *


# Sectors Ulrs
sectore_urls = patterns('',
    url(r'^crud/$', SectorsView.as_view(), name='sectors_view'),
)
subproject_urls = patterns('',
    url(r'^crud/$', SubprojectsView.as_view(), name='subproject_view'),
)
# Urls Projects
project_urls = patterns('',
    url(r'^$',ProjectsList.as_view(), name='view_projects'),
    url(r'^manager/(?P<project>\w+)/$', ProjectManager.as_view(), name='managerpro_view'),
    url(r'^sectors/', include(sectore_urls)),
    url(r'^subprojects/', include(subproject_urls)),
    url(r'^manager/sector/(?P<pro>\w+)/(?P<sub>.*)/(?P<sec>\w+)/$', SectorManage.as_view(), name='managersec_view'),
)

urlpatterns = patterns('',
    # url to home
    url(r'^$', SalesHome.as_view(), name='view_sale'),
    url(r'^projects/', include(project_urls)),
)