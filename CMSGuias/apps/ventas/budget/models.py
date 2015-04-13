from django.db import models

from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog

from CMSGuias.apps.home.models import Materiale, Unidade, Cargo, Tools
from CMSGuias.apps.tools.genkeys import generateGroupAnalysis


class AnalysisGroup(models.Model):
    agroup_id = models.CharField(max_length=5, default=generateGroupAnalysis(), primary_key=True)
    name = models.CharField(max_length=255)
    register = models.DateField(auto_now=True)
    flag = models.BooleanField(default=True)

    class Meta():
        ordering = ['register']


class Analysis(models.Model):
    analysis_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=255, null=False)
    unit = models.ForeignKey(Unidade, to_field='unidad_id')
    performance = models.FloatField()
    register = models.DateField(auto_now=True)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return '%s %s %s'%(self.analysis_id, self.name, self.register)

class APMaterials(models.Model):
    analysis = models.ForeignKey(Analysis, to_field='analysis_id')
    materials = models.ForeignKey(Materiale, to_field='materiales_id')
    quantity = models.FloatField(null=False)
    price = models.DecimalField(max_digits=5, decimal_places=3)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['materials']

    def __unicode__(self):
        return '%s %f %d'%(self.materials, self.quantity, self.price)

class APManPower(models.Model):
    analysis = models.ForeignKey(Analysis, to_field='analysis_id')
    manpower = models.ForeignKey(Cargo, to_field='cargo_id')
    gang = models.DecimalField(max_digits=3, decimal_places=2)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=3)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['manpower']

    def __unicode__(self):
        return '%s %s %d %d'%(self.analysis_id, self.manpower, self.quantity, self.price)

class APTools(models.Model):
    analysis = models.ForeignKey(Analysis, to_field='analysis_id')
    tools = models.ForeignKey(Tools, to_field='tools_id')
    gang = models.DecimalField(max_digits=3, decimal_places=2)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=3)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['tools']

    def __unicode__(self):
        return '%s %s %d %d'%(self.analysis_id, self.tools, self.quantity, self.price)

class Budget(models.Model):
    budget_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    register = models.DateField(auto_now=True)
    hourwork = models.IntegerField(default=0)
    finish = models.DateField()
    base = models.DecimalField(max_digits=10, decimal_places=3)
    offer = models.DecimalField(max_digits=10, decimal_places=3)
    observation = models.TextField()
    refecence = models.CharField(max_length=10)
    review = models.CharField(max_length=10)
    version = models.CharField(max_length=5, default='')
    status = models.CharField(max_length=2, default='PE')
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['budget_id']

    def __unicode__(self):
        return '%s %s'%(self.budget_id, self.name)

class BudgetItems(models.Model):
    budget = models.ForeignKey(Budget, to_field='budget_id')
    budgeti_id = models.CharField(max_length=13, primary_key=True)
    item =  models.DecimalField(max_digits=3, decimal_places=2)
    name = models.CharField(max_length=255)
    base = models.DecimalField(max_digits=10, decimal_places=3)
    offer = models.DecimalField(max_digits=10, decimal_places=3)
    tag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return '%s %s %s %d'%(self.budget_id, self.item, self.name, self.base)

class BudgetSub(models.Model):
    budget = models.ForeignKey(Budget, to_field='budget_id')
    budgeti = models.ForeignKey(BudgetItems, to_field='budgeti_id')
    budgetsub_id =  models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.ForeignKey(Unidade, to_field='unidad_id')
    status = models.CharField(default='PE', max_length=2)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['name']

class BudgetDetails(models.Model):
    budget = models.ForeignKey(Budget, to_field='budget_id')
    budgeti = models.ForeignKey(BudgetItems, to_field='budgeti_id')
    budgetsub =  models.ForeignKey(BudgetSub, to_field='budgetsub_id')
    analysis = models.ForeignKey(Analysis, to_field='analysis_id')
    quantity = models.FloatField()

    audit_log = AuditLog()

    class Meta:
        ordering = ['analysis']

    def __unicode__(self):
        return '%s %s %f'%(self.budget_id, self.analysis, self.quantity)