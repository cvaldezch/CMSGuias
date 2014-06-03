from django.contrib import admin
from CMSGuias.apps.logistica import models

admin.site.register(models.Cotizacion)
admin.site.register(models.CotCliente)
admin.site.register(models.DetCotizacion)
admin.site.register(models.CotKeys)
admin.site.register(models.tmpcotizacion)
admin.site.register(models.Compra)
admin.site.register(models.DetCompra)
admin.site.register(models.tmpcompra)
admin.site.register(models.DevProveedor)
admin.site.register(models.DetDevProveedor)