#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import *

budget_urls = patterns('',
    url(r'^analysis/prices/$',  NewAnalystPrices.as_view()),
)