#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import *
from .viewssec import *
from CMSGuias.apps.ventas.budget.urls import budget_urls


# Sectors Ulrs
sectore_urls = patterns(
    '',
    url(r'^crud/$', SectorsView.as_view(), name='sectors_view'),
)
subproject_urls = patterns(
    '',
    url(r'^crud/$', SubprojectsView.as_view(), name='subproject_view'),
)
# Urls Projects
project_urls = patterns(
    '',
    url(r'^$', ProjectsList.as_view(), name='view_projects'),
    url(r'^manager/(?P<project>\w+)/$',
        ProjectManager.as_view(), name='managerpro_view'),
    url(r'^sectors/', include(sectore_urls)),
    url(r'^subprojects/', include(subproject_urls)),
    url(r'^manager/sector/(?P<pro>\w+)/(?P<sub>\w+)/(?P<sec>\w+)/$',
        SectorManage.as_view(), name='managersec_view'),
    url(r'^services/(?P<pro>\w{7})/$',
        ServicesProjectView.as_view(), name='servicesp_view'),
    url(r'guide/list/(?P<pro>\w+)/(?P<sub>\w+)/(?P<sec>\w+)/$',
        ListGuideByProject.as_view(), name='view_list_guide_by_projects'),
    url(r'list/orders/(?P<pro>\w+)/(?P<sub>\w+)/(?P<sec>\w+)/$',
        ListOrdersByProject.as_view(), name='view_orders_by_projects'),
    url(r'^paint/(?P<pro>\w{7})/$', PaintingView.as_view(), 
        name='paintingp_view'),
    url(r'^closed/(?P<pro>\w{7})/$', ClosedProjectView.as_view(),
        name='closedproject_view'),
)

urlpatterns = patterns(
    '',
    url(r'^$', SalesHome.as_view(), name='view_sale'),
    url(r'^projects/', include(project_urls)),
    url(r'^budget/', include(budget_urls)),
)
