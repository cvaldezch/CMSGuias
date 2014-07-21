from django.db import models
from CMSGuias.apps.home.models import Pais, Departamento, Provincia, Distrito, Cliente, Materiale, Employee


class Proyecto(models.Model):
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
	empdni = models.ForeignKey(Employee, to_field='empdni_id', null=True, blank=True)
	flag = models.BooleanField(default=True,null=False)

	class Meta:
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
	status = models.CharField(max_length=2,null=False,default='00')
	flag = models.BooleanField(default=True,null=False)

	class Meta:
		ordering = ['nomsub']

	def __unicode__(self):
		return '%s - %s %s'%(self.proyecto,self.subproyecto_id,self.nomsub)

class Sectore(models.Model):
	sector_id = models.CharField(primary_key=True,max_length=20,null=False,unique=True)
	proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
	subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id',null=True)
	planoid = models.CharField(max_length=16,null=True,default='')
	nomsec = models.CharField(max_length=200)
	registrado = models.DateTimeField(auto_now=True,null=False)
	comienzo = models.DateField(null=True,blank=True)
	fin = models.DateField(null=True,blank=True)
	obser = models.TextField(null=True,blank=True)
	status = models.CharField(max_length=2,null=False,default='00')
	flag = models.BooleanField(default=True,null=False)

	class Meta:
		ordering = ['sector_id']

	def __unicode__(self):
		return '%s - %s %s'%(self.proyecto,self.subproyecto_id,self.sector_id)

class Metradoventa(models.Model):
	proyecto = models.ForeignKey(Proyecto, to_field='proyecto_id')
	subproyecto = models.ForeignKey(Subproyecto, to_field='subproyecto_id', null=True, blank=True)
	sector = models.ForeignKey(Sectore, to_field='sector_id')
	materiales = models.ForeignKey(Materiale, to_field='materiales_id')
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
	sector = models.ForeignKey(Sectore, to_field='sector_id')
	registrado = models.DateTimeField(auto_now=True)
	empdni = models.ForeignKey(Employee, to_field='empdni_id')
	cargo = models.CharField(max_length=3)
	mensage = models.TextField(max_length=250)
	flag = models.BooleanField(default=True)

	class Meta:
		ordering = ['proyecto']

	def __unicode__(self):
		return '%s %s %s %s %s'%(self.proyecto, self.sector, self.cargo, self.mensage, self.registrado)

