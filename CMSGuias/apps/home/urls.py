# -*- coding: utf-8 -*-
# from django.conf.urls.defaults import patterns, url
from django.conf.urls import patterns, url


urlpatterns = patterns('CMSGuias.apps.home.views',
	url(r'^SignUp/$','login_view',name="vista_login"),
	url(r'^$','view_home',name="vista_home"),
	url(r'^logout/$','logout_view',name="vista_logout"),
)