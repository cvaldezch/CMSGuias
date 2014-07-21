#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls import patterns, url, include

from .views import *


#Customers
customers_urls = patterns('',
    url(r'^list/$', CustomersList.as_view(), name='customers_list'),
    url(r'^new/$', CustomersCreate.as_view(), name='customers_new'),
    url(r'^edit/(?P<pk>\w+)/$', CustomersUpdate.as_view(), name='customers_edit'),
    url(r'^delete/(?P<pk>\w+)/$', CustomersDelete.as_view(), name='customers_del'),
)
# Country
country_urls = patterns('',
    url(r'^list/$', CountryList.as_view(), name='country_list'),
    url(r'^new/$', CountryCreate.as_view(), name='country_new'),
    url(r'^edit/(?P<pais_id>\w+)/$', CountryUpdate.as_view(), name='country_edit'),
    url(r'^delete/(?P<pais_id>\w+)/$', CountryDelete.as_view(), name='country_del'),
)
# Departament
departament_urls = patterns('',
    url(r'^list/$', DepartamentList.as_view(), name='departament_list'),
    url(r'^new/$', DepartamentCreate.as_view(), name='departament_new'),
    url(r'^edit/(?P<departamento_id>\w+)/$', DepartamentUpdate.as_view(), name='departament_edit'),
    url(r'^delete/(?P<departamento_id>\w+)/$', DepartamentDelete.as_view(), name='departament_del'),
)
# Province
province_urls = patterns('',
    url(r'^list/$', ProvinceList.as_view(), name='province_list'),
    url(r'^new/$', ProvinceCreate.as_view(), name='province_new'),
    url(r'^edit/(?P<provincia_id>\w+)/$', ProvinceUpdate.as_view(), name='province_edit'),
    url(r'^delete/(?P<provincia_id>\w+)/$', ProvinceDelete.as_view(), name='province_del'),
)
# District
district_urls = patterns('',
    url(r'^list/$', DistrictList.as_view(), name='district_list'),
    url(r'^new/$', DistrictCreate.as_view(), name='district_new'),
    url(r'^edit/(?P<distrito_id>\w+)/$', DistrictUpdate.as_view(), name='district_edit'),
    url(r'^delete/(?P<distrito_id>\w+)/$', DistrictDelete.as_view(), name='district_del'),
)
# urls main
urlpatterns = patterns('',
	url(r'^SignUp/$', LoginView.as_view(), name='vista_login'),
	url(r'^$', HomeManager.as_view(), name='vista_home'),
	url(r'^logout/$', LogoutView.as_view(), name='vista_logout'),
    url(r'^customers/', include(customers_urls)),
    url(r'^country/', include(country_urls)),
    url(r'^departament/', include(departament_urls)),
    url(r'^province/', include(province_urls)),
    url(r'^district/', include(district_urls)),
)