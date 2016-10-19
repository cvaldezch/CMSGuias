# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import PaintingData

urlpatterns = patterns(
    '',
    url(r'^paint/$', PaintingData.as_view(), name='viewPaint'),
)