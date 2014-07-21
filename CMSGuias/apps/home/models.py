#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class Pais(models.Model):
    pais_id = models.CharField(primary_key=True,max_length=3)
    paisnom = models.CharField(max_length=56)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['paisnom']

    def __unicode__(self):
        return self.paisnom

class Departamento(models.Model):
    departamento_id = models.CharField(primary_key=True, max_length=2)
    pais = models.ForeignKey(Pais, to_field='pais_id')
    depnom = models.CharField(max_length=56)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['depnom']

    def __unicode__(self):
        return self.depnom

class Provincia(models.Model):
    provincia_id = models.CharField(primary_key=True, max_length=3)
    departamento = models.ForeignKey(Departamento, to_field='departamento_id')
    pais = models.ForeignKey(Pais, to_field='pais_id')
    pronom = models.CharField(max_length=56)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['pronom']

    def __unicode__(self):
        return self.pronom

class Distrito(models.Model):
    distrito_id = models.CharField(primary_key=True, max_length=2)
    provincia = models.ForeignKey(Provincia, to_field='provincia_id')
    departamento = models.ForeignKey(Departamento, to_field='departamento_id')
    pais = models.ForeignKey(Pais, to_field='pais_id')
    distnom = models.CharField(max_length=56)
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['distnom']

    def __unicode__(self):
        return self.distnom

class Unidade(models.Model):
    unidad_id = models.CharField(primary_key=True,max_length=7)
    uninom = models.CharField(max_length=10)
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s'%(self.unidad_id,self.uninom)

class Materiale(models.Model):
    materiales_id = models.CharField(u'Mnemocode',unique=True,primary_key=True,max_length=15)
    matnom = models.CharField(max_length=200,null=False)
    matmed = models.CharField(max_length=200,null=False)
    unidad = models.ForeignKey(Unidade, to_field='unidad_id')
    matpre = models.FloatField(default=0,null=True)
    matmar = models.CharField(max_length=40,null=True)
    matmod = models.CharField(max_length=40,null=True)
    matacb = models.CharField(max_length=255,null=True)
    matare = models.FloatField(null=True)

    class Meta:
        ordering = ['matnom']

    def __unicode__(self):
        return '%s %s %s %s'%(self.materiales_id,self.matnom,self.matmed,self.unidad.uninom)

class Cargo(models.Model):
    cargo_id = models.CharField(primary_key=True, max_length=9)
    cargos = models.CharField(max_length=60)
    area = models.CharField(max_length=60, default='Nothing')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['cargos']

    def __unicode__(self):
        return '%s %s - %s'%(self.cargo_id, self.cargos, self.area)

class Employee(models.Model):
    empdni_id = models.CharField(primary_key=True, max_length=8)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=150)
    register = models.DateTimeField(auto_now=True)
    birth = models.DateField()
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=180)
    charge = models.ForeignKey(Cargo, to_field='cargo_id')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['lastname']

    def __unicode__(self):
        return '%s %s %s %s %s'%(self.empdni_id, self.firstname, self.lastname, self.phone, self.charge)

class userProfile(models.Model):
    def url(self,filename):
        ruta = "storage/Users/%s/%s"%(self.empdni,filename)
        return ruta

    user = models.OneToOneField(User)
    empdni = models.ForeignKey(Employee, to_field='empdni_id')
    photo = models.ImageField(upload_to=url, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

class Almacene(models.Model):
    almacen_id = models.CharField(primary_key=True,max_length=4)
    nombre = models.CharField(max_length=50,null=False)
    flag = models.BooleanField(default=True,null=False)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return "%s %s"%(self.almacen_id,self.nombre)

class Transportista(models.Model):
    traruc_id = models.CharField(primary_key=True,max_length=11)
    tranom = models.CharField(max_length=200,null=False)
    tratel = models.CharField(max_length=11,null=True,default='000-000-000')
    flag = models.BooleanField(default=True,null=False)

    def __unicode__(self):
        return "%s %s"%(self.traruc_id,self.tranom)

class Conductore(models.Model):
    traruc = models.ForeignKey(Transportista,to_field='traruc_id')
    condni_id = models.CharField(primary_key=True,max_length=8)
    connom = models.CharField(max_length=200,null=False)
    conlic = models.CharField(max_length=12,null=False)
    contel = models.CharField(max_length=11,null=True,default='',blank=True)
    flag = models.BooleanField(default=True,null=False)

    def __unicode__(self):
        return "%s %s %s"%(self.traruc,self.condni_id,self.connom)

class Transporte(models.Model):
    traruc = models.ForeignKey(Transportista,to_field='traruc_id')
    nropla_id = models.CharField(primary_key=True,max_length=8)
    marca = models.CharField(max_length=60,null=False)
    flag = models.BooleanField(default=True,null=False)

    def __unicode__(self):
        return "%s %s %s"%(self.traruc,self.nropla_id,self.marca)

class Cliente(models.Model):
    ruccliente_id = models.CharField(primary_key=True, max_length=11,null=False)
    razonsocial = models.CharField(max_length=200)
    pais = models.ForeignKey(Pais, to_field='pais_id')
    departamento = models.ForeignKey(Departamento, to_field='departamento_id')
    provincia = models.ForeignKey(Provincia, to_field='provincia_id')
    distrito = models.ForeignKey(Distrito, to_field='distrito_id')
    direccion = models.CharField(max_length=200,null=False,)
    telefono = models.CharField(max_length=11,null=True, blank=True,default='000-000-000')
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s'%(self.ruccliente_id,self.razonsocial)

    def get_absolute_url(self):
        return reverse('customers_edit', kwargs={'pk': self.ruccliente_id})

class Marca(models.Model): # Class Model de Marca de Materiales
    marca_id = models.CharField(primary_key=True, max_length=3, null=False)
    marca = models.CharField(max_length=40, null=False)
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s'%(self.marca_id,self.marca)

class ModelMarca(models.Model):
    modelo_id = models.CharField(primary_key=True, max_length=5)
    modelo = models.CharField(max_length=60)
    flag = models.BooleanField(default=True)

    def __unicode__(self):
      return '%s - %s'%(self.modelo_id, self.modelo)

class MarcaModelMaterial(models.Model):
    marca = models.ForeignKey(Marca, to_field='marca_id')
    modelo = models.ForeignKey(ModelMarca, to_field='modelo_id')
    matparcial = models.CharField(max_length=12, null=False)
    def __unicode__(self):
        return '%s %s'%(self.marca, self.matparcial)

class Herramientas(models.Model):
    herramientas_id = models.CharField(primary_key=True, max_length=14)
    herramientas = models.CharField(max_length=160, null=False)
    medida = models.CharField(max_length=160)
    unidad = models.ForeignKey(Unidade, to_field='unidad_id')
    tvida = models.IntegerField()
    acabado = models.CharField(max_length=13)

    def __unicode__(self):
        return '%s %s %s %s'%(self.herramientas_id, self.herramientas, self.medida, self.unidad)

class Documentos(models.Model):
    documento_id = models.CharField(primary_key=True, max_length=4)
    documento = models.CharField(max_length=160)
    tipo = models.CharField(max_length=2)
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s'%(self.documento_id,self.documento)

class FormaPago(models.Model):
    pagos_id = models.CharField(primary_key=True, max_length=4)
    pagos = models.CharField(max_length=160)
    valor = models.FloatField()
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s'%(self.pagos_id,self.pagos)

class Moneda(models.Model):
    moneda_id = models.CharField(primary_key=True,max_length=4)
    moneda = models.CharField(max_length=60)
    silbolo = models.CharField(max_length=3)
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s'%(self.moneda_id,self.moneda)

class TipoCambio(models.Model):
    moneda = models.ForeignKey(Moneda, to_field='moneda_id')
    fecha = models.DateField(auto_now=True)
    registrado = models.TimeField(auto_now=True)
    compra = models.FloatField()
    venta = models.FloatField()
    flag = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s'%(self.pagos_id,self.documento)

class Proveedor(models.Model):
    proveedor_id = models.CharField(primary_key=True, max_length=11)
    razonsocial = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    pais = models.ForeignKey(Pais, to_field='pais_id')
    departamento = models.ForeignKey(Departamento, to_field='departamento_id')
    provincia = models.ForeignKey(Provincia, to_field='provincia_id')
    distrito = models.ForeignKey(Distrito, to_field='distrito_id')
    telefono = models.CharField(max_length=12)
    tipo = models.CharField(max_length=8)
    origen = models.CharField(max_length=10)
    email = models.CharField(max_length=60, default='ejemplo@dominio.com')
    flag = models.BooleanField(default=True)

    def __unicode__(self):
      return '%s %s %s'%(self.proveedor_id, self.razonsocial, self.direccion)

class Configuracion(models.Model):
    periodo = models.CharField(max_length=4, default='')
    registrado = models.DateTimeField(auto_now=True)
    moneda = models.ForeignKey(Moneda, to_field='moneda_id')
    igv = models.IntegerField(default=10)

    def __unicode__(self):
        return "%s %s"%( self.periodo, self.moneda)