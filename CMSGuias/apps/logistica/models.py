# -*- coding: utf-8 -*-

from django.db import models

# import CMSGuias
from CMSGuias.apps.home.models import (
    Almacene,
    Documentos,
    FormaPago,
    Materiale,
    Moneda,
    Proveedor,
    Employee,
    Brand,
    Model,
    Unidade)
from CMSGuias.apps.ventas.models import Proyecto, Subproyecto
from CMSGuias.apps.tools import globalVariable
# from CMSGuias.apps.almacen.models import Suministro


class Cotizacion(models.Model):
    cotizacion_id = models.CharField(primary_key=True, max_length=10)
    suministro = models.ForeignKey(
        'almacen.Suministro', to_field='suministro_id', null=True, blank=True)
    empdni = models.ForeignKey(Employee, to_field='empdni_id')
    almacen = models.ForeignKey(Almacene, to_field='almacen_id')
    registrado = models.DateTimeField(auto_now_add=True)
    traslado = models.DateField()
    obser = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2, default='PE')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['cotizacion_id']

    def __unicode__(self):
        return '%s %s %s' % (self.cotizacion_id, self.almacen, self.traslado)


class Compra(models.Model):
    def url(self, filename):
        return 'storage/compra/%s/%s-%s.pdf' % (
            globalVariable.get_year, self.compra_id, self.proveedor_id)

    compra_id = models.CharField(primary_key=True, max_length=10)
    proveedor = models.ForeignKey(Proveedor, to_field='proveedor_id')
    empdni = models.ForeignKey(Employee, to_field='empdni_id', default='')
    cotizacion = models.ForeignKey(
        Cotizacion, to_field='cotizacion_id', null=True, blank=True)
    quotation = models.CharField(max_length=25, null=True, blank=True)
    projects = models.CharField(
        max_length=250, null=True, blank=True, default='')
    lugent = models.CharField(max_length=200, null=True, blank=True)
    documento = models.ForeignKey(
        Documentos, to_field='documento_id', null=True, blank=True)
    pagos = models.ForeignKey(
        FormaPago, to_field='pagos_id', null=True, blank=True)
    moneda = models.ForeignKey(
        Moneda, to_field='moneda_id', null=True, blank=True)
    registrado = models.DateTimeField(auto_now_add=True)
    traslado = models.DateField()
    contacto = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=2, default='PE')
    deposito = models.FileField(upload_to=url, null=True, blank=True)
    discount = models.FloatField(default=0, blank=True)
    # exchnage = models.DecimalField(max_digist=2, place_decimals=3)
    sigv = models.BooleanField(default=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['compra_id']

    def __unicode__(self):
        return '%s %s %s %s %s' % (
            self.compra_id,
            self.proveedor,
            self.documento,
            self.pagos,
            self.traslado)


class DetCompra(models.Model):
    compra = models.ForeignKey(Compra, to_field='compra_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(
        Brand, to_field='brand_id', default='BR000', blank=True)
    model = models.ForeignKey(
        Model, to_field='model_id', default='MO000', blank=True)
    cantidad = models.FloatField()
    precio = models.FloatField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # models.PositiveSmallIntegerField(default=0)
    cantstatic = models.FloatField()
    flag = models.CharField(max_length=1, default='0')
    perception = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f %f' % (
            self.compra, self.materiales, self.cantstatic, self.precio)


class tmpcompra(models.Model):
    empdni = models.CharField(max_length=8, null=False)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(
        Brand, to_field='brand_id', blank=True, default='BR000')
    model = models.ForeignKey(
        Model, to_field='model_id', blank=True, default='MO000')
    cantidad = models.FloatField(null=False)
    discount = models.PositiveSmallIntegerField(default=0)
    precio = models.FloatField(null=False, default=0)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f' % (self.empdni, self.materiales, self.cantidad)


class CotCliente(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, to_field='cotizacion_id')
    proveedor = models.ForeignKey(
        Proveedor, to_field='proveedor_id', null=True, blank=True)
    registrado = models.DateTimeField(auto_now_add=True)
    envio = models.DateField()
    contacto = models.CharField(max_length=200)
    validez = models.DateField()
    moneda = models.ForeignKey(Moneda, to_field='moneda_id')
    obser = models.TextField()
    status = models.CharField(max_length=2, default='PE')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['registrado']

    def __unicode__(self):
        return '%s %s %s' % (self.cotizacion, self.proveedor, self.contacto)


class DetCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, to_field='cotizacion_id')
    proveedor = models.ForeignKey(Proveedor, to_field='proveedor_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField()
    precio = models.FloatField(blank=True, default=0)
    discount = models.PositiveSmallIntegerField(blank=True, default=0)
    entrega = models.DateField(null=True, blank=True)
    marca = models.CharField(max_length=60, null=True, blank=True)
    modelo = models.CharField(max_length=60, null=True, blank=True)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %s %f %f' % (
            self.cotizacion_id,
            self.proveedor_id,
            self.materiales,
            self.cantidad,
            self.precio)

    @property
    def amount(self):
        if not self.precio:
            self.precio = 0
        if not self.discount:
            self.discount = 0
        precio = (self.precio - ((self.precio * self.discount) / 100))
        return (self.cantidad * precio)


class CotKeys(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, to_field='cotizacion_id')
    proveedor = models.ForeignKey(Proveedor, to_field='proveedor_id')
    keygen = models.CharField(max_length=12)
    status = models.CharField(max_length=2, default='PE')
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s %s' % (
            self.cotizacion_id, self.proveedor_id, self.keygen)


class tmpcotizacion(models.Model):
    empdni = models.CharField(max_length=8, null=False)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=False)
    brand = models.ForeignKey(
        Brand, to_field='brand_id', blank=True, default='BR000')
    model = models.ForeignKey(
        Model, to_field='model_id', blank=True, default='MO000')

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f' % (self.empdni, self.materiales, self.cantidad)


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
        return '%s %s %s' % (
            self.devolucionp_id, self.notaingreso, self.compra)


class DetDevProveedor(models.Model):
    devolucionp = models.ForeignKey(DevProveedor, to_field='devolucionp_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField()
    cantstatic = models.FloatField()
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f' % (
            self.devolucionp, self.materiales, self.cantstatic)


class ServiceOrder(models.Model):
    def url(self, filename):
        return 'storage/services/%s/%s-%s.pdf' % (
            globalVariable.get_year, self.serviceorder_id, self.supplier_id)

    serviceorder_id = models.CharField(max_length=10, primary_key=True)
    project = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subprojecto = models.ForeignKey(
                Subproyecto, to_field='subproyecto_id', null=True, blank=True)
    supplier = models.ForeignKey(Proveedor, to_field='proveedor_id')
    register = models.DateTimeField(auto_now_add=True)
    quotation = models.ForeignKey(
                Cotizacion, to_field='cotizacion_id', null=True, blank=True)
    arrival = models.CharField(max_length=250)
    document = models.ForeignKey(Documentos, to_field='documento_id')
    method = models.ForeignKey(FormaPago, to_field='pagos_id')
    start = models.DateField()
    term = models.DateField()
    dsct = models.FloatField(default=0, blank=True)
    currency = models.ForeignKey(Moneda, to_field='moneda_id')
    deposit = models.FileField(upload_to=url, null=True, blank=True)
    elaborated = models.ForeignKey(
                    Employee, related_name='elaboratedAsEmployee')
    authorized = models.ForeignKey(
                    Employee, related_name='authorizedAsEmployee')
    sigv = models.BooleanField(default=True, blank=True)
    status = models.CharField(max_length=2, default='PE')
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s %s %s' % (
            self.serviceorder_id, self.project, self.supplier, self.document)


class DetailsServiceOrder(models.Model):
    serviceorder = models.ForeignKey(ServiceOrder, to_field='serviceorder_id')
    description = models.TextField(null=False)
    unit = models.ForeignKey(Unidade, to_field='unidad_id')
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=3, default=0)

    @property
    def amount(self):
        return '%.3f' % (self.quantity * float(self.price))

    def __unicode__(self):
        return '%s %s %f' % (
            self.serviceorder,
            self.description,
            self.quantity)
