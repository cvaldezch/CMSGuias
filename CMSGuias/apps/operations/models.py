#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os

from django.db import models
from audit_log.models.managers import AuditLog

from CMSGuias.apps.home.models import Materiale, Brand, Model, Employee
from CMSGuias.apps.ventas.models import Proyecto, Subproyecto, Sectore
from CMSGuias.apps.tools import globalVariable


class MetProject(models.Model):
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id', default='')
    subproyecto = models.ForeignKey(Subproyecto,
                                    to_field='subproyecto_id',
                                    null=True,
                                    blank=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id')
    materiales = models.ForeignKey(
                                    Materiale,
                                    to_field='materiales_id',
                                    default='')
    brand = models.ForeignKey(Brand, to_field='brand_id', default='BR000')
    model = models.ForeignKey(Model, to_field='model_id', default='MO000')
    cantidad = models.FloatField()
    precio = models.FloatField()
    sales = models.DecimalField(max_digits=9, decimal_places=3, default=0)
    comment = models.CharField(
                                max_length=250,
                                default='',
                                null=True,
                                blank=True)
    quantityorder = models.FloatField(default=0)
    tag = models.CharField(max_length=1, default='0')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['proyecto']

    @property
    def amountPurchase(self):
        return float('{0:.3f}'.format(self.precio * self.cantidad))

    @property
    def amountSales(self):
        return float('{0:.3f}'.format(float(self.precio) * self.cantidad))

    def __unicode__(self):
        return '%s %s %s %f %f' % (
                                    self.proyecto,
                                    self.sector_id,
                                    self.materiales_id,
                                    self.cantidad,
                                    self.precio)


class Deductive(models.Model):
    REL = (
            ('NN', 'Nothing'),
            ('GL', 'Global'),
            ('ST', 'Un Sector'),
            ('PR', 'Personalido'),)
    deductive_id = models.CharField(primary_key=True, max_length=10)
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproyecto = models.ForeignKey(Subproyecto,
                                    to_field='subproyecto_id',
                                    null=True,
                                    blank=True)
    sector = models.ForeignKey(
                                Sectore,
                                to_field='sector_id',
                                null=True,
                                blank=True)
    register = models.DateTimeField(auto_now_add=True)
    rtype = models.CharField(max_length=3, choices=REL, default='NN')
    date = models.DateField(auto_now=True)
    relations = models.TextField()

    class Meta:
        ordering = ['deductive_id']


class DeductiveInputs(models.Model):
    deductive = models.ForeignKey(Deductive, to_field='deductive_id')
    date = models.DateField(auto_now=True)
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(Brand, to_field='brand_id', default='BR000')
    model = models.ForeignKey(Model, to_field='model_id', default='MO000')
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    related = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['deductive', 'materials']


class DeductiveOutputs(models.Model):
    deductive = models.ForeignKey(Deductive, to_field='deductive_id')
    date = models.DateField(auto_now=True)
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    # brand = models.ForeignKey(Brand, to_field='brand_id', default='BR000')
    # model = models.ForeignKey(Model, to_field='model_id', default='MO000')
    quantity = models.FloatField(default=0)
    # price = models.FloatField(default=0)
    # related = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['deductive', 'materials']


class Letter(models.Model):

    def url(self, filename):
        uri = 'storage/projects/%s/%s/letters/%s/%s.%s' % (
                self.project.registrado.strftime('%Y'),
                self.project_id,
                self.letter_id,
                self.letter_id,
                filename.split('.')[-1])
        name = '%s%s' % (globalVariable.relative_path, uri)
        if os.path.exists(name):
            os.remove(name)
        return uri

    letter_id = models.CharField(primary_key=True, max_length=19)
    project = models.ForeignKey(Proyecto, to_field='proyecto_id')
    register = models.DateTimeField(auto_now=True)
    performed = models.ForeignKey(Employee, to_field='empdni_id')
    froms = models.CharField(max_length=80)
    fors = models.CharField(max_length=80)
    status = models.CharField(max_length=2, default='PE')
    letter = models.FileField(
                                upload_to=url,
                                blank=True,
                                null=True,
                                max_length=200)
    observation = models.TextField(blank=True, null=True)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['letter_id']


class LetterAnexo(models.Model):
    def url(self, filename):
        return 'storage/projects/%s/%s/letters/%s/anexos/%s' % (
                    self.letter.project.registrado.strftime('%Y'),
                    self.letter.project_id,
                    self.letter_id,
                    filename)
    letter = models.ForeignKey(Letter, to_field='letter_id')
    anexo = models.FileField(
                                upload_to=url,
                                max_length=200,
                                blank=True,
                                null=True)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['letter']


class PreOrders(models.Model):
    preorder_id = models.CharField(primary_key=True, max_length=10)
    project = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproject = models.ForeignKey(
                                    Subproyecto,
                                    to_field='subproyecto_id',
                                    blank=True,
                                    null=True)
    sector = models.ForeignKey(
                                Sectore,
                                to_field='sector_id',
                                blank=True,
                                null=True)
    performed = models.ForeignKey(Employee, to_field='empdni_id')
    register = models.DateTimeField(auto_now=True)
    transfer = models.DateField()
    issue = models.CharField(max_length=200)
    observation = models.TextField(null=True, blank=True)
    nipples = models.TextField(null=True, blank=True)
    annular = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, default='PE')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['preorder_id']

    def __unicode__(self):
        return '%s %s %s' % (self.preorder_id, self.performed, self.issue)


class DetailsPreOrders(models.Model):
    preorder = models.ForeignKey(PreOrders, to_field='preorder_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    quantity = models.FloatField()
    orders = models.FloatField()

    def __unicode__(self):
        return '%s %s %f' % (self.preorder, self.materials, self.quantity)


class SGroup(models.Model):
    sgroup_id = models.CharField(
                                primary_key=True,
                                max_length=13,
                                default='PRAA000SG0000',
                                unique=False)
    project = models.ForeignKey(Proyecto, to_field='proyecto_id')
    subproject = models.ForeignKey(
                                    Subproyecto,
                                    to_field='subproyecto_id',
                                    blank=True,
                                    null=True)
    sector = models.ForeignKey(Sectore, to_field='sector_id')
    name = models.CharField(max_length=255)
    register = models.DateTimeField(auto_now_add=True)
    datestart = models.DateField(null=True, blank=True)
    dateend = models.DateField(null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    colour = models.CharField(max_length=21, blank=True, null=True)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    def __unicode__(self):
        return '%s - %s %s' % (self.sgroup_id, self.name, self.register)


class DSector(models.Model):
    def url(self, filename):
        return 'storage/projects/%s/%s/%s/%s.pdf' % (
                self.project.registrado.strftime('%Y'),
                self.project_id,
                self.sgroup_id,
                self.dsector_id)

    dsector_id = models.CharField(
                                    primary_key=True,
                                    max_length=18,
                                    default='PRAA000SG0000DS000')
    sgroup = models.ForeignKey(SGroup, to_field='sgroup_id')
    project = models.ForeignKey(Proyecto, to_field='proyecto_id')
    name = models.CharField(max_length=255)
    plane = models.FileField(
                            upload_to=url,
                            max_length=200, null=True, blank=True)
    register = models.DateTimeField(auto_now_add=True)
    datestart = models.DateField(null=True)
    dateend = models.DateField(null=True)
    description = models.TextField(null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, default='PE', blank=True)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    def __unicode__(self):
        return '%s %s %s %s' % (self.project,
                                self.dsector_id,
                                self.name,
                                self.register)


class DSMetrado(models.Model):
    dsector = models.ForeignKey(DSector, to_field='dsector_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    quantity = models.FloatField()
    qorder = models.FloatField()
    qguide = models.FloatField()
    ppurchase = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    psales = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    comment = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=1, default='0')
    nipple = models.BooleanField(default=False, blank=True)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        verbose_name = 'SMetrado'
        verbose_name_plural = 'SMetrados'

    def __unicode__(self):
        return '%s %s %f %f' % (self.dsector_id,
                                self.materials,
                                self.quantity,
                                self.ppurchase)


class MMetrado(models.Model):
    register = models.DateTimeField(auto_now=True, null=True)
    dsector = models.ForeignKey(DSector, to_field='dsector_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    quantity = models.FloatField()
    qorder = models.FloatField()
    qguide = models.FloatField()
    ppurchase = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    psales = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    comment = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=1, default='0')
    nipple = models.BooleanField(default=False, blank=True)
    flag = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'MMetrado'
        verbose_name_plural = 'MMetrados'

    def __unicode__(self):
        return '%s %s %f' % (self.dsector_id, self.materials, self.quantity)


class HistoryDSMetrado(models.Model):
    qcode = models.CharField(max_length=16)
    register = models.DateTimeField(auto_now=True)
    dsector = models.ForeignKey(DSector, to_field='dsector_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    brand = models.ForeignKey(Brand, to_field='brand_id')
    model = models.ForeignKey(Model, to_field='model_id')
    quantity = models.FloatField()
    qorder = models.FloatField()
    qguide = models.FloatField()
    ppurchase = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    psales = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    comment = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=1, default='0')
    nipple = models.BooleanField(default=False, blank=True)
    flag = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'SMetrado'
        verbose_name_plural = 'SMetrados'

    def __unicode__(self):
        return '%s %s %f %f' % (self.dsector_id,
                                self.materials,
                                self.quantity,
                                self.ppurchase)


class Nipple(models.Model):
    proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id', blank=True)
    subproyecto = models.ForeignKey(
                                    Subproyecto,
                                    to_field='subproyecto_id',
                                    blank=True,
                                    null=True)
    sector = models.ForeignKey(
                                Sectore,
                                to_field='sector_id',
                                blank=True,
                                null=True)
    area = models.ForeignKey(
            DSector,
            to_field='dsector_id',
            null=True,
            blank=True)
    materiales = models.ForeignKey(Materiale, to_field='materiales_id')
    cantidad = models.FloatField(null=True, default=1)
    metrado = models.FloatField(null=False, default=0)
    cantshop = models.FloatField(null=True, default=0)
    tipo = models.CharField(max_length=1)
    comment = models.CharField(
                                max_length=250,
                                default='',
                                null=True,
                                blank=True)
    tag = models.CharField(max_length=1, default='0')
    flag = models.BooleanField(default=True)

    class Meta:
        ordering = ['proyecto']

    def __unicode__(self):
        return '%s %s %f %f %s' % (
            self.proyecto_id,
            self.materiales_id,
            self.cantidad,
            self.metrado,
            self.tipo)
