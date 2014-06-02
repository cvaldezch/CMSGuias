from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pais(models.Model):
	pais_id = models.CharField(primary_key=True,max_length=3)
	paisnom = models.CharField(max_length=56)
	flag = models.BooleanField(default=True)
	def __unicode__(self):
		return self.paisnom

class Departamento(models.Model):
	departamento_id = models.CharField(primary_key=True, max_length=2)
	pais = models.ForeignKey(Pais, to_field='pais_id')
	depnom = models.CharField(max_length=56)
	flag = models.BooleanField(default=True)

	def __unicode__(self):
		return self.depnom

class Provincia(models.Model):
	provincia_id = models.CharField(primary_key=True, max_length=3)
	departamento = models.ForeignKey(Departamento, to_field='departamento_id')
	pais = models.ForeignKey(Pais, to_field='pais_id')
	pronom = models.CharField(max_length=56)
	flag = models.BooleanField(default=True)

	def __unicode__(self):
		return self.pronom

class Distrito(models.Model):
	distrito_id = models.CharField(primary_key=True, max_length=2)
	provincia = models.ForeignKey(Provincia, to_field='provincia_id')
	departamento = models.ForeignKey(Departamento, to_field='departamento_id')
	pais = models.ForeignKey(Pais, to_field='pais_id')
	distnom = models.CharField(max_length=56)
	flag = models.BooleanField(default=True)

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

class userProfile(models.Model):
	def url(self,filename):
		ruta = "MutimediaData/Users/%s/%s"%(self.user.username,filename)
		return ruta

	user = models.OneToOneField(User)
	empdni = models.CharField(max_length=8,null=False)
	photo = models.ImageField(upload_to=url,null=True)

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
	flag = models.BooleanField(default=True,null=False)

	def __unicode__(self):
		return '%s %s'%(self.ruccliente_id,self.razonsocial)
