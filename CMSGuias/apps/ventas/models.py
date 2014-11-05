from django.db import models

from CMSGuias.apps.home.models import Pais, Departamento, Provincia, Distrito, Cliente, Materiale, Employee, Brand, Model, Cargo, Moneda, Documentos, FormaPago, Unidade
from CMSGuias.apps.tools import globalVariable, search


class Proyecto(models.Model):
    STATUS_PROJECT = (('PE','PEDIENTE'),('AC', 'ACTIVO'),('CO', 'COMPLETO'),)
    proyecto_id = models.CharField(primary_key=True, max_length=7,null=False)
    ruccliente = models.ForeignKey(Cliente, to_field='ruccliente_id',null=True)
    nompro = models.CharField(max_length=200)
    registrado = models.DateTimeField(auto_now=True,null=False)
    comienzo = models.DateField(null=True)
    fin = models.DateField(null=True,blank=True)
    pais = models.ForeignKey(Pais, to_field='pais_id')
    departamento = models.ForeignKey(Departamento, to_field='departamento_id')
    provincia = models.ForeignKey(Provincia, to_field='provincia_id')
    distrito = models.ForeignKey(Distrito, to_field='distrito_id')
    direccion = models.CharField(max_length=200,null=False)
    obser = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=2,null=False,default='00')
    empdni = models.ForeignKey(Employee, related_name='proyectoAsEmployee', null=True, blank=True)
    approved = models.ForeignKey(Employee, related_name='approvedAsEmployee', null=True, blank=True)
    currency = models.ForeignKey(Moneda, to_field='moneda_id', null=True, blank=True)
    exchange = models.FloatField(null=True, blank=True)
    flag = models.BooleanField(default=True, null=False)

    class Meta:
        #abstract = True
        ordering = ['nompro']

    def __unicode__(self):
        return '%s %s - %s'%(self.proyecto_id,self.nompro,self.ruccliente_id)

class Subproyecto(models.Model):
    subproyecto_id = models.CharField(primary_key=True,max_length=7,null=False)
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    nomsub = models.CharField(max_length=200)
    registrado = models.DateTimeField(auto_now=True)
    comienzo = models.DateField(null=True,blank=True)
    fin = models.DateField(null=True,blank=True)
    obser = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=2,null=False,default='AC')
    additional = models.BooleanField(blank=True, default=False)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['nomsub']

    def __unicode__(self):
        return '%s - %s %s'%(self.proyecto,self.subproyecto_id,self.nomsub)

class Sectore(models.Model):
    sector_id = models.CharField(primary_key=True,max_length=20,null=False,unique=True)
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id',null=True, blank=True)
    planoid = models.CharField(max_length=16,null=True,default='')
    nomsec = models.CharField(max_length=200)
    registrado = models.DateTimeField(auto_now=True)
    comienzo = models.DateField(null=True,blank=True)
    fin = models.DateField(null=True,blank=True)
    obser = models.TextField(null=True,blank=True)
    amount = models.FloatField(default=0, blank=True, null=True)
    atype = models.CharField(max_length=2, default='NN', blank=True)
    link = models.TextField(default='', blank=True)
    status = models.CharField(max_length=2,null=False,default='AC')
    flag = models.BooleanField(default=True, null=False)

    class Meta:
        ordering = ['sector_id']

    def __unicode__(self):
        return '%s - %s %s'%(self.proyecto,self.subproyecto,self.sector_id)

class SectorFiles(models.Model):
    def url(self, filename):
        if self.subproyecto is None:
            ruta = 'storage/projects/%s/%s/%s/%s'%(globalVariable.get_year,self.proyecto_id,self.sector_id,filename)
        else:
            ruta = 'storage/projects/%s/%s/%s/%s/%s'%(globalVariable.get_year,self.proyecto_id, self.subproyecto_id,self.sector_id,filename)
        return ruta

    sector = models.ForeignKey(Sectore, to_field='sector_id')
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id',null=True, blank=True)
    files = models.FileField(upload_to=url, max_length=200)
    note = models.TextField(default='', blank=True)
    date = models.DateField(auto_now=True, default=globalVariable.getToday.date())
    time = models.TimeField(auto_now=True, default=globalVariable.getToday.time())
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s - %s'%(self.sector, self.files)

class Metradoventa(models.Model):
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id', null=True, blank=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(Brand, to_field='brand_id', default='BR000')
    model = models.ForeignKey(Model, to_field='model_id', default='MO000')
    cantidad = models.FloatField()
    precio = models.FloatField()
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['proyecto']

    def __unicode__(self):
        return '%s %s %s %f %f'%(self.proyecto, self.sector, self.materiales, self.cantidad, self.precio)

class Alertasproyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id', null=True, blank=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id', null=True, blank=True)
    registrado = models.DateTimeField(auto_now_add=True)
    empdni = models.ForeignKey(Employee, to_field='empdni_id')
    charge = models.ForeignKey(Cargo, to_field='cargo_id')
    message = models.TextField(default='')
    status = models.CharField(max_length=8, default='success')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['proyecto']

    def __unicode__(self):
        return '%s %s %s %s %s'%(self.proyecto, self.sector, self.charge, self.message, self.registrado)

class HistoryMetProject(models.Model):
    date = models.DateField(auto_now=True)
    token = models.CharField(max_length=6, default=globalVariable.get_Token())
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id', default='')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id', null=True, blank=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id', default='')
    brand = models.ForeignKey(Brand, to_field='brand_id', default='BR000')
    model = models.ForeignKey(Model, to_field='model_id', default='MO000')
    quantity = models.FloatField()
    price = models.FloatField()
    comment = models.CharField(max_length=250,default='',null=True, blank=True)
    quantityorders = models.FloatField(default=0)
    tag = models.CharField(max_length=1, default='0')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['proyecto']

    def __unicode__(self):
        return '%s %s %s %f %f'%(self.proyecto, self.sector, self.materials_id, self.quantity, self.price)

class RestoreStorage(models.Model):
    date = models.DateField(auto_now=True)
    token = models.CharField(max_length=6, default=globalVariable.get_Token())
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id', default='')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id', null=True, blank=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id', default='')
    brand = models.ForeignKey(Brand, to_field='brand_id', default='BR000')
    model = models.ForeignKey(Model, to_field='model_id', default='MO000')
    quantity = models.FloatField()
    price = models.FloatField()
    tag = models.CharField(max_length=1, default='0')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['proyecto']

    def __unicode__(self):
        return '%s %s %s %f %f'%(self.proyecto, self.sector, self.materials_id, self.quantity, self.price)

class UpdateMetProject(models.Model):
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id', default='')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id', null=True, blank=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id', default='')
    brand = models.ForeignKey(Brand, to_field='brand_id', default='BR000')
    model = models.ForeignKey(Model, to_field='model_id', default='MO000')
    quantity = models.FloatField()
    price = models.FloatField()
    comment = models.CharField(max_length=250, default='',null=True, blank=True)
    quantityorders = models.FloatField(default=0, blank=True)
    tag = models.CharField(max_length=1, default='0')
    flag = models.BooleanField(default=True)

    @property
    def amount(self):
        return (self.quantity * self.price)

    class Meta:
        ordering = ['proyecto']

    def __unicode__(self):
        return '%s %s %s %f %f'%(self.proyecto, self.sector, self.materials_id, self.quantity, self.price)

class PurchaseOrder(models.Model):
    def url(self, filename):
        ruta = "storage/projects/%s/%s/purchase_order_customers/%s.pdf"%(search.searchPeriodProject(self.project_id),self.project_id,self.nropurchase)
        return ruta

    project = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproject = models.ForeignKey(Subproyecto, to_field='subproyecto_id',null=True, blank=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id')
    nropurchase = models.CharField(max_length=14)
    issued = models.DateField()
    currency = models.ForeignKey(Moneda, to_field='moneda_id')
    document = models.ForeignKey(Documentos, to_field='documento_id')
    method = models.ForeignKey(FormaPago, to_field='pagos_id')
    observation = models.TextField(null=True, blank=True)
    dsct = models.FloatField(default=0, blank=True)
    igv = models.FloatField(default=0, blank=True)
    order = models.FileField(upload_to=url,null=True, blank=True, max_length=200)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['project']

    def __unicode__(self):
        return '%s - %s'%(self.project, self.purchase_id)

class DetailsPurchaseOrder(models.Model):
    purchase = models.ForeignKey(PurchaseOrder, to_field='id')
    nropurchase = models.CharField(max_length=14)
    description = models.CharField(max_length=250)
    unit = models.ForeignKey(Unidade, to_field='unidad_id')
    delivery = models.DateField()
    quantity = models.FloatField()
    price = models.FloatField()

    class Meta:
        ordering = ['nropurchase']
