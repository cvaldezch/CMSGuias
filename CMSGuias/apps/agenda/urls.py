#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='diaryview'),
    url(r'^employee/$', EmployeeView.as_view(), name='diaryemployeeview'),
)
