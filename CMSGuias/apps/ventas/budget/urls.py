#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import *

groupAnalysis = patterns('',
                         url(r'^add/$',
                             addAnalysisGroup.as_view(),
                             name='addanalysisgroup'),
                         url(r'^list/$', AnalysisGroupList.as_view(),
                             name='listanalysisgroup'),
                         url(r'^details/(?P<analysis>\w+)/$',
                             AnalysisDetails.as_view(),
                             name='detailsamalysis'),
                         )

budget_urls = patterns('',
                       url(r'^analysis/group/', include(groupAnalysis)),
                       url(r'^analysis/prices/$',  AnalystPrices.as_view(),
                           name='analysisprice_view'),
                       url(r'^$', BudgetView.as_view(), name='budget_view'),
                       )
