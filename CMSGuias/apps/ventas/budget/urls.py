#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import *

groupAnalysis = patterns(
    '',
    url(r'^add/$', addAnalysisGroup.as_view(), name='addanalysisgroup'),
    url(r'^list/$', AnalysisGroupList.as_view(), name='listanalysisgroup'),
    url(r'^details/(?P<analysis>\w+)/$', AnalysisDetails.as_view(),
        name='detailsamalysis'),
)

budgeturi = patterns(
  '',
  url(r'^$', BudgetView.as_view(), name='budget_view'),
  url(r'^body/(?P<budget>\w{10})/(?P<rev>\w{5})/$',
      BudgetItemsView.as_view(), name='items_view'),
)

budget_urls = patterns(
    '',
    url(r'^analysis/group/', include(groupAnalysis)),
    url(r'^analysis/prices/$', AnalystPrices.as_view(),
        name='analysisprice_view'),
    url(r'^', include(budgeturi)),
)
