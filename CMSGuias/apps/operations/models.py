#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.db import models

from CMSGuias.apps.home.models import Materiale, Brand, Model
from CMSGuias.apps.ventas.models import Proyecto, Subproyecto, Sectore


class MetProject(models.Model):
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id', default='')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id', null=True, blank=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id')
    materiales = models.ForeignKey(Materiale, to_field='materiales_id', default='')
    brand = models.ForeignKey(Brand, to_field='brand_id', default='BR000')
    model = models.ForeignKey(Model, to_field='model_id', default='MO000')
    cantidad = models.FloatField()
    precio = models.FloatField()
    comment = models.CharField(max_length=250,default='',null=True, blank=True)
    quantityorder = models.FloatField(default=0)
    tag = models.CharField(max_length=1, default='0')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['proyecto']

    def __unicode__(self):
        return '%s %s %s %f %f'%(self.proyecto, self.sector, self.materiales, self.cantidad, self.precio)

class Nipple(models.Model):
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id',blank=True,null=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id',blank=True,null=True)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=True,default=1)
    metrado = models.FloatField(null=False, default=0)
    cantshop = models.FloatField(null=True, default=0)
    tipo = models.CharField(max_length=1)
    comment = models.CharField(max_length=250, default='', null=True, blank=True)
    tag = models.CharField(max_length=1,default='0')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['proyecto']

    def __unicode__(self):
        return ''