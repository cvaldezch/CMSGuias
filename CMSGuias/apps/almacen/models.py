from django.db import connection, models, transaction

from CMSGuias.apps.ventas.models import Proyecto, Subproyecto, Sectore
from CMSGuias.apps.home.models import Materiale, Almacene, Transportista, Transporte, Conductore, Cliente, Brand, Model, Employee


class Pedido(models.Model):
    def url(self,filename):
        ruta = "storage/pedido/%s/%s.pdf"%(self.proyecto_id,self.pedido_id)
        return ruta

    pedido_id = models.CharField(primary_key=True,max_length=10,default='PEAA000000')
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id',blank=True,null=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id',blank=True,null=True)
    almacen = models.ForeignKey(Almacene, to_field='almacen_id')
    asunto = models.CharField(max_length=160,null=True)
    empdni = models.CharField(max_length=8,null=False)
    registrado = models.DateTimeField(auto_now=True)
    traslado = models.DateField()
    obser = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=2,null=False,default='36')
    flag = models.BooleanField(default=True)
    orderfile = models.FileField(upload_to=url,null=True,blank=True)

    def __unicode__(self):
        return '%s %s'%(self.pedido_id,self.proyecto.nompro)

class Detpedido(models.Model):
    pedido = models.ForeignKey(Pedido, to_field='pedido_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=False)
    cantshop = models.FloatField(default=0,null=False)
    cantguide = models.FloatField(default=0,null=True,blank=True)
    tag = models.CharField(max_length=1,default='0',null=False)
    spptag = models.BooleanField(default=False)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f'%(self.pedido.pedido_id,self.materiales.materiales_id,self.cantidad)

class tmppedido(models.Model):
    empdni = models.CharField(max_length=8, null=False)
    materiales = models.ForeignKey(Materiale,to_field='materiales_id')
    cantidad = models.FloatField(null=False)

    def __unicode__(self):
        return '%s %s %f'%(self.empdni, self.materiales, self.cantidad)

class Niple(models.Model):
    pedido = models.ForeignKey(Pedido, to_field='pedido_id')
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id',blank=True,null=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id',blank=True,null=True)
    empdni = models.CharField(max_length=8,null=False)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=True,default=1)
    metrado = models.FloatField(null=False, default=0)
    cantshop = models.FloatField(null=True, default=0)
    cantguide= models.FloatField(default=0,null=True, blank=True)
    tipo = models.CharField(max_length=1)
    flag = models.BooleanField(default=True)
    tag = models.CharField(max_length=1,default='0')
    comment = models.CharField(max_length=250, default='', null=True, blank=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s'%(self.materiales,self.proyecto.nompro)

class tmpniple(models.Model):
    empdni = models.ForeignKey(Employee, to_field='empdni_id')
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id', null=True, blank=True)
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id', null=True, blank=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id', null=True, blank=True)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=True, default=1)
    metrado = models.FloatField(null=False, default=1)
    tipo = models.CharField(max_length=1)
    comment = models.CharField(max_length=250, null=True, blank=True, default='')
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s'%(self.materiales,self.metrado)

class GuiaRemision(models.Model):
    guia_id = models.CharField(primary_key=True,max_length=12)
    pedido = models.ForeignKey(Pedido, to_field='pedido_id')
    ruccliente = models.ForeignKey(Cliente, to_field='ruccliente_id')
    puntollegada = models.CharField(max_length=200,null=True)
    registrado = models.DateTimeField(auto_now=True)
    traslado = models.DateField(null=False)
    traruc = models.ForeignKey(Transportista, to_field='traruc_id')
    condni = models.ForeignKey(Conductore, to_field='condni_id')
    nropla = models.ForeignKey(Transporte, to_field='nropla_id')
    status = models.CharField(max_length=2, default='46')
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s %s'%(self.guia_id,self.pedido.pedido_id,self.ruccliente.razonsocial)

class DetGuiaRemision(models.Model):
    guia = models.ForeignKey(GuiaRemision, to_field='guia_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantguide = models.FloatField(default=0,null=True,blank=True)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f'%(self.guia.guia_id,self.materiales.materiales_id,self.cantguide)

class NipleGuiaRemision(models.Model):
    guia = models.ForeignKey(GuiaRemision, to_field='guia_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    metrado = models.FloatField(null=False, default=0)
    cantguide = models.FloatField(default=0,null=True, blank=True)
    tipo = models.CharField(max_length=1)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s'%(self.materiales,self.guia)

class Suministro(models.Model):
    suministro_id = models.CharField(primary_key=True, max_length=10)
    almacen = models.ForeignKey(Almacene, to_field='almacen_id')
    empdni = models.CharField(max_length=8)
    asunto = models.CharField(max_length=180, null=True, blank=True)
    registrado = models.DateTimeField(auto_now=True)
    ingreso = models.DateField()
    obser = models.TextField()
    status = models.CharField(max_length=2, default='PE')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['suministro_id']

    def __unicode__(self):
        return '%s %s %s'%(self.suministro_id,self.almacen,self.ingreso)

class DetSuministro(models.Model):
    suministro = models.ForeignKey(Suministro, to_field='suministro_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=False)
    cantshop = models.FloatField(default=0,null=False)
    tag = models.CharField(max_length=1,default='0',null=False)
    origin = models.CharField(max_length=10,default='NN')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    def __unicode__(self):
        return '%s %s %f'%(self.suministro, self.materiales, self.cantidad)

class tmpsuministro(models.Model):
    empdni = models.CharField(max_length=8, null=False)
    materiales = models.ForeignKey(Materiale,to_field='materiales_id')
    cantidad = models.FloatField(null=False)
    origin = models.CharField(max_length=2,default='NN', null=True)
    origin_id = models.CharField(max_length=10,null=True,blank=True)

    def __unicode__(self):
        return '%s %s %f'%(self.empdni,self.materiales,self.cantidad)

class Inventario(models.Model):
    materiales = models.ForeignKey(Materiale,to_field='materiales_id')
    almacen = models.ForeignKey(Almacene, to_field='almacen_id')
    precompra = models.FloatField()
    preventa = models.FloatField(default=0)
    stkmin = models.FloatField()
    stock = models.FloatField()
    stkpendiente = models.FloatField()
    stkdevuelto = models.FloatField()
    periodo = models.CharField(max_length=4, default='')
    ingreso = models.DateField(auto_now=True)
    compra = models.ForeignKey('logistica.Compra', to_field='compra_id', null=True,blank=True)
    spptag = models.BooleanField(default=False)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materiales']

    @staticmethod
    @transaction.commit_on_success
    def register_all_list_materilas(alid,quantity):
      try:
          cn = connection.cursor() # Open connection to DDBB
          cn.callproc('SP_almacen_RegisterListMaterials',[alid,quantity,]) # Execute Store Procedure
          result = cn.fetchone() # recover result
          cn.close() # close connection
          return result[0]
      except Exception, e:
          print e
          transaction.rollback()
          return False

    @staticmethod
    @transaction.commit_on_success
    def register_period_past(alid,period,almacen):
      try:
          cn = connection.cursor() # Open connection to DDBB
          cn.callproc('sp_almacen_registerperiod',[alid,period,almacen,]) # Execute Store Procedure
          result = cn.fetchone() # recover result
          cn.close() # close connection
          return result[0]
      except Exception, e:
          transaction.rollback()
          return False

    def __unicode__(self):
        return '%s %s %f'%(self.materiales,self.compra,self.stock)

class InventoryBrand(models.Model):
    period = models.CharField(max_length=4)
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    ingress = models.DateTimeField(auto_now=True)
    stock = models.FloatField()
    purchase = models.FloatField()
    sale = models.FloatField()
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['materials']

    def __unicode__(self):
        return '%s %s %s %f'%(self.materials,self.period,self.brand,self.stock)
