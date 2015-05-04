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
# Brand
brand_urls = patterns('',
    url(r'^list/$', BrandList.as_view(), name='brand_list'),
    url(r'^new/$', BrandCreate.as_view(), name='brand_new'),
    url(r'^edit/(?P<brand_id>\w+)/$', BrandUpdate.as_view(), name='brand_edit'),
    url(r'^delete/(?P<brand_id>\w+)/$', BrandDelete.as_view(), name='brand_del'),
)
# Model
model_urls = patterns('',
    url(r'^list/$', ModelList.as_view(), name='model_list'),
    url(r'^new/$', ModelCreate.as_view(), name='model_new'),
    url(r'^edit/(?P<model_id>\w+)/$', ModelUpdate.as_view(), name='model_edit'),
    url(r'^delete/(?P<model_id>\w+)/$', ModelDelete.as_view(), name='model_del'),
)
# Type Group Materials
tgroup_urls = patterns('',
    url(r'^list/$', TGroupList.as_view(), name='tgroup_list'),
    url(r'^new/$', TGroupCreate.as_view(), name='tgroup_new'),
    url(r'^edit/(?P<tgroup_id>\w+)/$', TGroupUpdate.as_view(), name='tgroup_edit'),
    url(r'^delete/(?P<tgroup_id>\w+)/$', TGroupDelete.as_view(), name='tgroup_del'),
)
# Type Group Materials
gmaterials_urls = patterns('',
    url(r'^list/$', GMaterialsList.as_view(), name='gmaterials_list'),
    url(r'^new/$', GMaterialsCreate.as_view(), name='gmaterials_new'),
    url(r'^edit/(?P<mgroup_id>\w+)/$', GMaterialsUpdate.as_view(), name='gmaterials_edit'),
    url(r'^edit/save/(?P<mgroup_id>\w+)/$', GMaterialsUpdateSave.as_view(), name='gmaterials_edit_save'),
    url(r'^delete/(?P<mgroup_id>\w+)/$', GMaterialsDelete.as_view(), name='gmaterials_del'),
    url(r'^details/(?P<mgroup>\w+)/$', DetailsGMaterials.as_view(), name='gmaterials_details'),
)
# Crud Materials
materials_urls = patterns('',
    url(r'^$', MaterialsKeep.as_view(), name='materials_view'),
)
# Crud Unit
unit_urls = patterns('',
    url(r'^add/$', UnitAdd.as_view(), name='unit_add'),
    # url(r'^edit/(?P<unit>\w+)/$', ),
    # url(r'^del/(?P<unit>\w+)/$', ),
    url(r'^list/$', Unit.as_view(), name='unit_list'),
)
# Crud Cargos y/o ManPower
manpower_urls = patterns('',
    url(r'^list/cbo/$', ManPower.as_view(), name='manpower_cbolist'),
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
    url(r'^brand/', include(brand_urls)),
    url(r'^model/', include(model_urls)),
    url(r'^tgroup/', include(tgroup_urls)),
    url(r'^gmaterials/', include(gmaterials_urls)),
    url(r'^materials/', include(materials_urls)),
    url(r'^unit/', include(unit_urls)),
    url(r'^manpower/', include(manpower_urls)),
)