#-*- Encoding: utf-8 -*-
from django import forms
from CMSGuias.apps.almacen import models

# Customers
class addCustomersForm(forms.ModelForm ):
	class Meta:
		model   = models.Cliente
		exclude = {"flag",}
		widgets = {
							'ruccliente_id': forms.TextInput(attrs ={'class': 'form-control'}),
							'razonsocial': forms.TextInput(attrs   ={'class': 'form-control'}),
							'pais': forms.Select(attrs             ={'class': 'form-control'}),
							'departamento': forms.Select(attrs     ={'class': 'form-control'}),
							'provincia': forms.Select(attrs        ={'class': 'form-control'}),
							'distrito': forms.Select(attrs         ={'class': 'form-control'}),
							'direccion': forms.Textarea(attrs      ={'class': 'form-control', 'maxlength': '200', 'rows': '4'}),
							'telefono': forms.TextInput(attrs      ={'type':'tel','placeholder':'000-000-000','class': 'form-control'}),
							}
# Projects
class addProjectForm(forms.ModelForm):
	class Meta:
		model   = models.Proyecto
		exclude = {"flag","proyecto_id",}
		STATUS  = (("AC", "ACTIVE"),)
		widgets = {
							"ruccliente": forms.Select(attrs    ={'class': 'form-control'}),
							"nompro": forms.TextInput(attrs     ={'class': 'form-control'}),
							"comienzo": forms.TextInput(attrs   ={'class': 'form-control in-date',"maxlength":"10","placeholder":"aaaa-mm-dd"}),
							"fin": forms.TextInput(attrs        ={'class': 'form-control in-date',"maxlength":"10","placeholder":"aaaa-mm-dd"}),
							"pais": forms.Select(attrs          ={'class': 'form-control'}),
							"departamento": forms.Select(attrs  ={'class': 'form-control'}),
							"provincia": forms.Select(attrs     ={'class': 'form-control'}),
							"distrito": forms.Select(attrs      ={'class': 'form-control'}),
							"direccion": forms.TextInput(attrs  ={'class': 'form-control'}),
							"obser": forms.Textarea(attrs       ={'class': 'form-control', 'maxlength': '200', 'rows': '4'}),
							"status": forms.Select(attrs        ={'class': 'form-control'}, choices=STATUS),
							}
# sectores
class addSectoresForm(forms.ModelForm):
	def __ini__(self,*args,**kwargs):
		super(addSectoresForm, self).__init__(*args,**kwargs)
		self.proid = kwargs.pop("proid")
		print proid
	class Meta:
		model   = models.Sectore
		exclude = {"registrado","flag","proyecto","subproyecto",}
		STATUS  = (("AC","ACTIVE"),)		
		widgets ={
						"sector_id": forms.TextInput(attrs ={'class': 'form-control'}),                                                   
						#"proyecto": forms.Select(attrs     ={'class': 'form-control'}),                                                       
						#"subproyecto": forms.Select(attrs  ={'class': 'form-control'}),                                                    
						"planoid": forms.TextInput(attrs   ={'class': 'form-control'}),                                                     
						"nomsec": forms.TextInput(attrs    ={'class': 'form-control'}),                                                      
						"comienzo": forms.TextInput(attrs  ={'class': 'form-control in-date',"maxlength":"10","placeholder":"aaaa-mm-dd"}),
						"fin": forms.TextInput(attrs       ={'class': 'form-control in-date',"maxlength":"10","placeholder":"aaaa-mm-dd"}),     
						"obser": forms.Textarea(attrs      ={'class': 'form-control', 'maxlength':'200','rows':'3'}),
						"status": forms.Select(attrs       ={'class': 'form-control'}, choices=STATUS),
						}
# SubProyectos'
class addSubprojectForm(forms.ModelForm):
	class Meta:
		model   = models.Subproyecto
		exclude = {"proyecto","registrado","flag",}
		STATUS  = (("AC","ACTIVE"),)
		widgets = {
						"subproyecto_id": forms.TextInput(attrs ={'class': 'form-control'}),
						"nomsub": forms.TextInput(attrs         ={'class': 'form-control'}),
						"comienzo": forms.TextInput(attrs       ={'class': 'form-control in-date',"maxlength":"10","placeholder":"aaaa-mm-dd"}),
						"fin": forms.TextInput(attrs            ={'class': 'form-control in-date',"maxlength":"10","placeholder":"aaaa-mm-dd"}),
						"obser": forms.Textarea(attrs           ={'class': 'form-control', 'maxlength':'200','rows':'3'}),
						"status": forms.Select(attrs            ={'class': 'form-control'}, choices=STATUS),
		}
# Almacenes
class addAlmacenesForm(forms.ModelForm):
	class Meta:
		model = models.Almacene
		exclude = { "almacen_id","flag", }
		widgets= {
							"nombre": forms.TextInput(attrs = {'class': 'form-control', 'maxlength':'50'}),
		}