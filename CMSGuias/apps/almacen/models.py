# -*- coding: utf-8 -*-
#
from audit_log.models.managers import AuditLog
from django.db import connection, models, transaction
from CMSGuias.apps.ventas.models import Proyecto, Subproyecto, Sectore
from CMSGuias.apps.operations.models import DSector
from CMSGuias.apps.home.models import (
                                        Materiale,
                                        Almacene,
                                        Transportista,
                                        Transporte,
                                        Conductore,
                                        Cliente,
                                        Brand,
                                        Model,
                                        Employee)
from CMSGuias.apps.logistica.models import Compra


class Pedido(models.Model):
    def url(self, filename):
        ext = filename.split('.')[-1]
        year = self.proyecto.registrado.strftime('%Y')
        ruta = 'storage/projects/%s/%s/orders/%s.%s' % (
                year,
                self.proyecto_id,
                self.pedido_id,
                ext)
        return ruta

    pedido_id = models.CharField(
                    primary_key=True, max_length=10, default='PEAA000000')
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(
                    Subproyecto, to_field='subproyecto_id',
                    blank=True, null=True)
    sector = models.ForeignKey(
                Sectore, to_field='sector_id', blank=True, null=True)
    dsector = models.ForeignKey(
                DSector, to_field='dsector_id', blank=True, null=True)
    almacen = models.ForeignKey(Almacene, to_field='almacen_id')
    asunto = models.CharField(max_length=160, null=True)
    empdni = models.ForeignKey(
                Employee, to_field='empdni_id', null=True, default='70492850')
    # models.CharField(max_length=8,null=False)
    registrado = models.DateTimeField(auto_now_add=True)
    traslado = models.DateField()
    obser = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, null=False, default='PE')
    flag = models.BooleanField(default=True)
    orderfile = models.FileField(upload_to=url, null=True, blank=True)

    audit_log = AuditLog()

    def __unicode__(self):
        return '%s %s' % (self.pedido_id, self.proyecto.nompro)


class Detpedido(models.Model):
    pedido = models.ForeignKey(Pedido, to_field='pedido_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(
                Brand, to_field='brand_id', default='BR000', blank=True, null=False)
    model = models.ForeignKey(
                Model, to_field='model_id', default='MO000', blank=True, null=False)
    cantidad = models.FloatField(null=False)
    cantshop = models.FloatField(default=0, null=False)
    cantguide = models.FloatField(default=0, null=True, blank=True)
    tag = models.CharField(max_length=1, default='0', null=False)
    spptag = models.BooleanField(default=False)
    comment = models.CharField(max_length=250, default='', null=True)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f' % (
            self.pedido.pedido_id,
            self.materiales.materiales_id, self.cantidad)


class tmppedido(models.Model):
    empdni = models.CharField(max_length=8, null=False)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=False)
    brand = models.ForeignKey(
                Brand, to_field='brand_id', default='BR000', blank=True, null=False)
    model = models.ForeignKey(
                Model, to_field='model_id', default='MO000', blank=True, null=False)

    def __unicode__(self):
        return '%s %s %f' % (self.empdni, self.materiales, self.cantidad)


class Niple(models.Model):
    pedido = models.ForeignKey(Pedido, to_field='pedido_id')
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(
                    Subproyecto, to_field='subproyecto_id',
                    blank=True, null=True)
    sector = models.ForeignKey(
                Sectore, to_field='sector_id', blank=True, null=True)
    dsector = models.ForeignKey(
                DSector, to_field='dsector_id', blank=True, null=True)
    empdni = models.CharField(max_length=8, null=False)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(
            Brand, to_field='brand_id', blank=True, default='BR000', null=False)
    model = models.ForeignKey(
            Model, to_field='model_id', blank=True, default='MO000', null=False)
    cantidad = models.FloatField(null=True, default=1)
    metrado = models.FloatField(null=False, default=0)
    cantshop = models.FloatField(null=True, default=0)
    cantguide = models.FloatField(default=0, null=True, blank=True)
    tipo = models.CharField(max_length=1)
    flag = models.BooleanField(default=True)
    tag = models.CharField(max_length=1, default='0')
    comment = models.CharField(
                max_length=250, default='', null=True, blank=True)
    related = models.IntegerField(null=True, blank=True, default=0)

    audit_log = AuditLog()

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s' % (self.materiales, self.proyecto.nompro)


class tmpniple(models.Model):
    empdni = models.ForeignKey(Employee, to_field='empdni_id')
    proyecto = models.ForeignKey(
                Proyecto, to_field='proyecto_id', null=True, blank=True)
    subproyecto = models.ForeignKey(
                    Subproyecto, to_field='subproyecto_id',
                    null=True, blank=True)
    sector = models.ForeignKey(
                Sectore, to_field='sector_id', null=True, blank=True)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(
            Brand, to_field='brand_id', blank=True, default='BR000', null=False)
    model = models.ForeignKey(
            Model, to_field='model_id', blank=True, default='MO000', null=False)
    cantidad = models.FloatField(null=True, default=1)
    metrado = models.FloatField(null=False, default=1)
    tipo = models.CharField(max_length=1)
    comment = models.CharField(
                max_length=250, null=True, blank=True, default='')
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s' % (self.materiales, self.metrado)


class GuiaRemision(models.Model):
    guia_id = models.CharField(primary_key=True, max_length=12)
    pedido = models.ForeignKey(
                Pedido, to_field='pedido_id', null=True, blank=True)
    ruccliente = models.ForeignKey(Cliente, to_field='ruccliente_id')
    puntollegada = models.CharField(max_length=200, null=True)
    registrado = models.DateTimeField(auto_now_add=True)
    traslado = models.DateField(null=False)
    traruc = models.ForeignKey(Transportista, to_field='traruc_id')
    condni = models.ForeignKey(Conductore, to_field='condni_id')
    nropla = models.ForeignKey(Transporte, to_field='nropla_id')
    status = models.CharField(max_length=2, default='46')
    motive = models.CharField(max_length=160, default='VENTA', blank=True)
    comment = models.TextField(default='')
    observation = models.CharField(max_length=250, null=True, blank=True)
    nota = models.CharField(max_length=250, null=True, blank=True)
    dotoutput = models.CharField(max_length=250, null=True, blank=True)
    orders = models.CharField(max_length=250, null=True, blank=True, default=None)
    flag = models.BooleanField(default=True)
    perreg = models.ForeignKey(Employee, to_field='empdni_id', null=True, blank=True)

    audit_log = AuditLog()

    def __unicode__(self):
        return '%s %s' % (
            self.guia_id, self.ruccliente.razonsocial)


class DetGuiaRemision(models.Model):
    guia = models.ForeignKey(GuiaRemision, to_field='guia_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantguide = models.FloatField(default=0, null=True, blank=True)
    brand = models.ForeignKey(
                Brand, to_field='brand_id', blank=True, default='BR000')
    model = models.ForeignKey(
                Model, to_field='model_id', blank=True, default='MO000')
    obrand = models.ForeignKey(
                Brand, related_name='obrandAsDetGuide', blank=True, default='BR000')
    omodel = models.ForeignKey(
                Model, related_name='omodelAsDetGuide', blank=True, default='MO000')
    observation = models.CharField(max_length=250, null=True, blank=True)
    order = models.ForeignKey(Pedido, to_field='pedido_id', null=True, blank=True)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f' % (
            self.guia.guia_id, self.materiales.materiales_id, self.cantguide)


class TmpDetGuia(models.Model):
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    quantity = models.FloatField(default=0, null=True, blank=True)
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    observation = models.CharField(max_length=250, null=True, blank=True)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materials']

    def __unicode__(self):
        return '%s %f' % (self.materiales.materiales_id, self.quantity)


class NipleGuiaRemision(models.Model):
    guia = models.ForeignKey(GuiaRemision, to_field='guia_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(
            Brand, to_field='brand_id', blank=True, default='BR000', null=False)
    model = models.ForeignKey(
            Model, to_field='model_id', blank=True, default='MO000', null=False)
    metrado = models.FloatField(null=False, default=0)
    cantguide = models.FloatField(default=0, null=True, blank=True)
    tipo = models.CharField(max_length=1)
    flag = models.BooleanField(default=True)
    related = models.IntegerField(null=True, blank=True, default=0)
    order = models.ForeignKey(Pedido, to_field='pedido_id', null=True, blank=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s' % (self.materiales, self.guia)


class Suministro(models.Model):
    suministro_id = models.CharField(primary_key=True, max_length=10)
    almacen = models.ForeignKey(Almacene, to_field='almacen_id')
    empdni = models.CharField(max_length=8)
    asunto = models.CharField(max_length=180, null=True, blank=True)
    registrado = models.DateTimeField(auto_now_add=True)
    ingreso = models.DateField()
    obser = models.TextField()
    status = models.CharField(max_length=2, default='PE')
    orders = models.CharField(max_length=250, blank=True, default='')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['suministro_id']

    def __unicode__(self):
        return '%s %s %s' % (self.suministro_id, self.almacen, self.ingreso)


class DetSuministro(models.Model):
    suministro = models.ForeignKey(Suministro, to_field='suministro_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=False)
    cantshop = models.FloatField(default=0, null=False)
    brand = models.ForeignKey(
            Brand, to_field='brand_id', default='BR000', blank=True, null=True)
    model = models.ForeignKey(
            Model, to_field='model_id', default='MO000', blank=True, null=True)
    tag = models.CharField(max_length=1, default='0', null=False)
    origin = models.CharField(max_length=10, default='NN')
    # orders = models.CharField(max_length=250, blank=True, default='')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f' % (self.suministro, self.materiales, self.cantidad)


class tmpsuministro(models.Model):
    empdni = models.CharField(max_length=8, null=False)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=False)
    brand = models.ForeignKey(Brand, to_field='brand_id', default='BR000')
    model = models.ForeignKey(Model, to_field='model_id', default='MO000')
    origin = models.CharField(max_length=2, default='NN', null=True)
    orders = models.ForeignKey(
                Pedido, to_field='pedido_id', null=True, blank=True)

    def __unicode__(self):
        return '%s %s %f' % (self.empdni, self.materiales, self.cantidad)


class Inventario(models.Model):
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    almacen = models.ForeignKey(Almacene, to_field='almacen_id')
    precompra = models.FloatField()
    preventa = models.FloatField(default=0)
    stkmin = models.FloatField()
    stock = models.FloatField()
    stkpendiente = models.FloatField()
    stkdevuelto = models.FloatField()
    periodo = models.CharField(max_length=4, default='')
    ingreso = models.DateField(auto_now=True)
    compra = models.ForeignKey(
            'logistica.Compra',
            to_field='compra_id',
            null=True,
            blank=True)
    spptag = models.BooleanField(default=False)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['materiales']

    @staticmethod
    @transaction.commit_on_success
    def register_all_list_materilas(alid, quantity):
        try:
            cn = connection.cursor()
            # Open connection to DDBB
            cn.callproc('SP_almacen_RegisterListMaterials', [alid, quantity, ])
            result = cn.fetchone()
            # recover result
            cn.close()
            return result[0]
        except Exception, e:
            print e
            transaction.rollback()
            return False

    @staticmethod
    @transaction.commit_on_success
    def register_period_past(alid, period, almacen):
        try:
            print 'print call proc'
            cn = connection.cursor()
            # Open connection to DDBB
            cn.callproc('sp_almacen_registerperiod', [alid, period, almacen, ])
            result = cn.fetchone()
            # recover result
            print result
            cn.close()
            return result[0]
        except Exception, e:
            print e
            transaction.rollback()
            return False

    def __unicode__(self):
        return '%s %s %f' % (self.materiales, self.compra, self.stock)


class InventoryBrand(models.Model):
    storage = models.ForeignKey(Almacene, to_field='almacen_id')
    period = models.CharField(max_length=4)
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    ingress = models.DateTimeField(auto_now=True)
    stock = models.FloatField()
    purchase = models.FloatField()
    sale = models.FloatField()
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['materials']

    @staticmethod
    @transaction.commit_on_success
    def eraseAllInventory():
        cn = connection.cursor()
        try:
            cn.callproc('proc_erase_all_inventory')
            return cn.fetchone()[0]
        except Exception, e:
            transaction.rollback()
            return str(e)
        finally:
            cn.close()

    def __unicode__(self):
        return '%s %s %s %f' % (
            self.materials, self.period, self.brand, self.stock)


class NoteIngress(models.Model):
    ingress_id = models.CharField(primary_key=True, max_length=10)
    storage = models.ForeignKey(Almacene, to_field='almacen_id')
    purchase = models.ForeignKey(Compra, to_field='compra_id')
    guide = models.CharField(max_length=12, null=True, blank=True)
    invoice = models.CharField(max_length=12, null=True, blank=True)
    motive = models.CharField(max_length=60, blank=True)
    register = models.DateTimeField(auto_now=True)
    receive = models.ForeignKey(Employee, related_name='receiveAsEmployee')
    inspection = models.ForeignKey(
                    Employee, related_name='inspectionAsEmployee')
    approval = models.ForeignKey(Employee, related_name='approvalAsEmployee')
    observation = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, default='IN')
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()


class DetIngress(models.Model):
    ingress = models.ForeignKey(NoteIngress, to_field='ingress_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    quantity = models.FloatField()
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    report = models.CharField(max_length=1, default='0')
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()


class ReportInspect(models.Model):
    inspect = models.CharField(primary_key=True, max_length=10)
    ingress = models.ForeignKey(NoteIngress, to_field='ingress_id')
    transport = models.CharField(max_length=60)
    arrival = models.DateField()
    instorage = models.DateField()
    register = models.DateTimeField(auto_now_add=True)
    boarding = models.CharField(max_length=10)
    description = models.TextField()
    observation = models.TextField(null=True, blank=True)
    empdni = models.ForeignKey(Employee, to_field='empdni_id')


class Restoration(models.Model):
    restoration_id = models.CharField(max_length=6, primary_key=True)
    almacen = models.ForeignKey(Almacene, to_field='almacen_id', blank=True)
    register = models.DateTimeField(auto_now_add=True)
    ndocument = models.ForeignKey(GuiaRemision, to_field='guia_id')
    observation = models.TextField()
    performed = models.ForeignKey(Employee, to_field='empdni_id')
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    def __unicode__(self):
        return '%s %s' % (self.restoration_id, self.register)


class DetRestoration(models.Model):
    restoration = models.ForeignKey(Restoration, to_field='restoration_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    quantity = models.FloatField()

    class Meta:
        ordering = ['materials']

    def __unicode__(self):
        return '%s %s' % (self.restoration_id, self.materials_id)

class ReturnItemsProject(models.Model):
    pedido = models.ForeignKey(Pedido, to_field='pedido_id')
    register = models.DateTimeField(auto_now_add=True)
    observation = models.TextField(null=True, blank=True)
    listsend = models.TextField(null=False)
    notpro = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, default='AC')

    class Meta:
        ordering = ['-register']

    def __unicode__(self):
        return '%s %s %s' % (self.pedido.pedido_id, self.register, self.observation)

class Balance(models.Model):
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    storage = models.ForeignKey(Almacene, to_field='almacen_id',  default='AL01', blank=True)
    register = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    balance = models.FloatField()

    audit_log = AuditLog()

    class Meta:
        ordering = ['-register']

    def __unicode__(self):
        return '%s %s %s %f' % (self.materials_id, self.brand.brand, self.model.model, self.balance)
