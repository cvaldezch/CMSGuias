from django.contrib import admin
from CMSGuias.apps.almacen import models

admin.site.register(models.Detpedido)
admin.site.register(models.DetGuiaRemision)
admin.site.register(models.GuiaRemision)
admin.site.register(models.Niple)
admin.site.register(models.NipleGuiaRemision)
admin.site.register(models.Pedido)
admin.site.register(models.tmpniple)
admin.site.register(models.tmppedido)
admin.site.register(models.Inventario)
admin.site.register(models.Suministro)
admin.site.register(models.DetSuministro)
admin.site.register(models.tmpsuministro)