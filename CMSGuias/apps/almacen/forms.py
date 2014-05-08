#-*- Encoding: utf-8 -*-
from django import forms
from CMSGuias.apps.almacen import models

# Customers
class addCustomersForm(forms.ModelForm ):
	class Meta:
		model = models.Cliente
		exclude = {"flag",}
		widgets = {
							'ruccliente_id': forms.TextInput(attrs={'class': 'form-control'}),
							'razonsocial': forms.TextInput(attrs={'class': 'form-control'}),
							'pais': forms.Select(attrs={'class': 'form-control'}),
							'departamento': forms.Select(attrs={'class': 'form-control'}),
							'provincia': forms.Select(attrs={'class': 'form-control'}),
							'distrito': forms.Select(attrs={'class': 'form-control'}),
							'direccion': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '200', 'rows': '4'}),
							'telefono': forms.TextInput(attrs={'class': 'form-control'}),
							}