from django.db import models
from CMSGuias.apps.home.models import Almacene, Documentos, FormaPago, Materiale, Moneda, Proveedor
from CMSGuias.apps.almacen.models import Suministro

# Create your models here.

class Cotizacion(models.Model):
    cotizacion_id = models.CharField(primary_key=True, max_length=10)
    suministro = models.ForeignKey(Suministro, to_field='suministro_id', null=True, blank=True)
    empdni = models.CharField(max_length=8)
    almacen = models.ForeignKey(Almacene, to_field='almacen_id')
    registrado = models.DateTimeField(auto_now=True)
    traslado = models.DateField()
    obser = models.TextField()
    status = models.CharField(max_length=2,default='PE')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['cotizacion_id']

    def __unicode__(self):
        return '%s %s %s'%(self.cotizacion, self.almacen, self.traslado)

class CotCliente(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, to_field='cotizacion_id')
    proveedor = models.ForeignKey(Proveedor, to_field='proveedor_id', null=True, blank=True)
    registrado = models.DateTimeField(auto_now=True)
    envio = models.DateField()
    contacto = models.CharField(max_length=200)
    validez = models.DateField()
    moneda = models.ForeignKey(Moneda, to_field='moneda_id')
    obser = models.TextField()
    status = models.CharField(max_length=2,default='PE')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['registrado']

    def __unicode__(self):
        return '%s %s %s'%(self.cotizacion, self.proveedor, self.contacto)

class DetCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, to_field='cotizacion_id')
    proveedor = models.ForeignKey(Proveedor, to_field='proveedor_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField()
    precio = models.FloatField()
    entrega = models.DateField()
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %s %f %f'%(self.cotizacion, self.proveedor, self.materiales, self.cantidad, self.precio)

class CotKeys(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, to_field='cotizacion_id')
    proveedor = models.ForeignKey(Proveedor, to_field='proveedor_id')
    keygen = models.CharField(max_length=12)
    status = models.CharField(max_length=2,default='PE')
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s %s'%(self.cotizacion, self.proveedor, self.keygen)

class tmpcotizacion(models.Model):
    empdni = models.CharField(max_length=8, null=False)
    materiales = models.ForeignKey(Materiale,to_field='materiales_id')
    cantidad = models.FloatField(null=False)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f'%(self.empdni,self.materiales,self.cantidad)

class Compra(models.Model):
    compra_id = models.CharField(primary_key=True, max_length=10)
    proveedor = models.ForeignKey(Proveedor, to_field='proveedor_id')
    empdni = models.CharField(max_length=8)
    cotizacion = models.ForeignKey(Cotizacion, to_field='cotizacion_id')
    lugent = models.CharField(max_length=200)
    documento = models.ForeignKey(Documentos, to_field='documento_id')
    pagos = models.ForeignKey(FormaPago, to_field='pagos_id')
    moneda = models.ForeignKey(Moneda, to_field='moneda_id')
    registrado = models.DateTimeField(auto_now=True)
    traslado = models.DateField()
    contacto = models.CharField(max_length=200)
    status = models.CharField(max_length=2, default='PE')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['compra_id']

    def __unicode__(self):
        return '%s %s %s %s %s'%(self.compra_id, self.proveedor, self.documento, self.pago, self.traslado)

class DetCompra(models.Model):
    compra = models.ForeignKey(Compra, to_field='compra_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField()
    precio = models.FloatField()
    cantstatic = models.FloatField()
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f %f'%(self.compra, self.materiales, self.cantstatic, self.precio)

class tmpcompra(models.Model):
    empdni = models.CharField(max_length=8, null=False)
    materiales = models.ForeignKey(Materiale,to_field='materiales_id')
    cantidad = models.FloatField(null=False)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f'%(self.empdni, self.materiales, self.cantidad)

class DevProveedor(models.Model):
    devolucionp_id = models.CharField(primary_key=True, max_length=10)
    notaingreso = models.CharField(max_length=10)
    almacen = models.ForeignKey(Almacene, to_field='almacen_id')
    compra = models.ForeignKey(Compra, to_field='compra_id')
    notacredido = models.CharField(max_length=10) 
    montonc = models.FloatField()
    obser = models.TextField()
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['devolucionp_id']

    def __unicode__(self):
        return '%s %s %s'%(self.devolucionp_id, self.notaingreso, self.compra)

class DetDevProveedor(models.Model):
    devolucionp = models.ForeignKey(DevProveedor, to_field='devolucionp_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField()
    cantstatic = models.FloatField()
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f'%(self.devolucionp, self.materiales, self.cantstatic)
