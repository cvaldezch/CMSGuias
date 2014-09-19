from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'', include('CMSGuias.apps.home.urls')),
    url(r'^almacen/', include('CMSGuias.apps.almacen.urls')),
    url(r'^logistics/', include('CMSGuias.apps.logistica.urls')),
    url(r'^json/', include('CMSGuias.apps.wsjson.urls')),
    url(r'^reports/', include('CMSGuias.apps.reports.urls')),
    url(r'^sales/', include('CMSGuias.apps.ventas.urls')),
    url(r'^operations/', include('CMSGuias.apps.operations.urls')),
    url(r'^proveedor/', include('CMSGuias.apps.suppliers.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
