#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns(
    '',
    url(r'^$', OperationsHome.as_view(), name='home_operations'),
    url(
        r'^list/preorders/(?P<pro>\w{7})/(?P<sub>\w+|)/(?P<sec>\w+)/$',
        ListPreOrders.as_view(),
        name='view_list_preordersop'),
    url(r'sector/group/(?P<pro>\w{7})/(?P<sub>\w+|)/(?P<sec>\w+)/$',
        ProgramingProject.as_view(), name='sectorgroup_view'),
    url(r'area/(?P<sgroup>\w+)/(?P<area>\w+)/(?P<pro>\w+)/(?P<sec>\w+)/(?P<sub>\w+)/$',
        AreaProjectView.as_view(), name='dsector_view'),
)
