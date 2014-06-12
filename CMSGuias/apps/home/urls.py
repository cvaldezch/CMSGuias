# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

import views


urlpatterns = patterns('CMSGuias.apps.home.views',
	url(r'^SignUp/$','login_view',name="vista_login"),
	url(r'^$',views.HomeManager.as_view(),name="vista_home"),
	url(r'^logout/$','logout_view',name="vista_logout"),
)