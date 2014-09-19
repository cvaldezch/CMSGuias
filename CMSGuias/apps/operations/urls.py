#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import *

urlpatterns = patterns('',
    # url to home
    url(r'^$', OperationsHome.as_view(), name='home_operations'),
)