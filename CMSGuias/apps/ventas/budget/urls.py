#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import *

groupAnalysis = patterns('',
    url(r'^add/$', addAnalysisGroup.as_view(), name='addanalysisgroup'),
    #url(r'^list/$', AnalysisGroup.as_view(), name='listanalysisgroup'),
)

budget_urls = patterns('',
    url(r'^analysis/group/', include(groupAnalysis)),
    url(r'^analysis/prices/$',  NewAnalystPrices.as_view()),
)