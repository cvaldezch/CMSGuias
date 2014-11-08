#!/usr/bin/env python
#-*- Encoding: utf-8 -*-
#
from django import forms
from django.contrib.auth.models import User

from .models import *


class logininForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class signupForm(forms.Form):
	""" por algun motivo no funciona """
	class Meta:
		model = User
		fields = ['username', 'password']
		widget = {
			'password' : forms.PasswordInput(render_value=False),
		}

# Customers
class CustomersForm(forms.ModelForm):
    class Meta:
        EMPTY = (('', '-- Nothing --'),)
        exclude = { 'flag', }
        model = Cliente
        widgets = {
            'ruccliente_id': forms.TextInput(attrs = {'class': 'form-control'}),
            'razonsocial': forms.TextInput(attrs = {'class': 'form-control'}),
            'pais': forms.Select(attrs = {'class': 'form-control'}),
            'departamento': forms.Select(attrs = {'class': 'form-control'}, choices=EMPTY),
            'provincia': forms.Select(attrs = {'class': 'form-control'}, choices=EMPTY),
            'distrito': forms.Select(attrs = {'class': 'form-control'}, choices=EMPTY),
            'direccion': forms.Textarea(attrs = {'class': 'form-control', 'maxlength': '200', 'rows': '4'}),
            'telefono': forms.TextInput(attrs = {'type':'tel','placeholder':'000-000-000','class': 'form-control'}),
        }

# Country
class CountryForm(forms.ModelForm):
    class Meta:
        exclude = {'flag',}
        model = Pais
        widgets = {
            'pais_id': forms.TextInput(attrs={'class': 'form-control'}),
            'paisnom': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Departament
class DepartamentForm(forms.ModelForm):
    class Meta:
        exclude = {'flag',}
        model = Departamento
        widgets = {
            'pais' : forms.Select(attrs = {'class' : 'form-control'}),
            'departamento_id' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'depnom' : forms.TextInput(attrs = {'class' : 'form-control'}),
        }

# Province
class ProvinceForm(forms.ModelForm):
    class Meta:
        exclude = {'flag',}
        model = Provincia
        widgets = {
            'pais' : forms.Select(attrs = {'class' : 'form-control'}),
            'departamento' : forms.Select(attrs = {'class' : 'form-control'}),
            'provincia_id' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'pronom' : forms.TextInput(attrs = {'class' : 'form-control'})
        }

# District
class DistrictForm(forms.ModelForm):
    class Meta:
        exclude = {'flag',}
        model = Distrito
        widgets = {
            'pais' : forms.Select(attrs = {'class' : 'form-control'}),
            'departamento' : forms.Select(attrs = {'class' : 'form-control'}),
            'provincia' : forms.Select(attrs = {'class' : 'form-control'}),
            'distrito_id' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'distnom' : forms.TextInput(attrs = {'class' : 'form-control'}),
        }

# Brand
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        exclude = {'brand_id','flag',}
        widgets = {
            'brand' : forms.TextInput(attrs = {'class': 'form-control'}),
        }

# Model
class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        exclude = {'model_id','flag'}
        widgets = {
            'brand' : forms.Select(attrs = {'class':'form-control'}),
            'model' : forms.TextInput(attrs = {'class':'form-control'}),
        }

# Type Group
class TGroupForm(forms.ModelForm):
    class Meta:
        model = TypeGroup
        exclude = {'tgroup_id','flag'}
        widgets = {
            'typeg' : forms.TextInput(attrs = {'class':'form-control'}),
        }

class GMaterialsForm(forms.ModelForm):
    class Meta:
        model = GroupMaterials
        exclude = {'mgroup_id', 'flag',}
        widgets = {
            'tgroup': forms.Select(attrs = {'class': 'form-control'}),
            'description': forms.TextInput(attrs = {'class': 'form-control'}),
            'materials_id': forms.Select(attrs = {'class': 'form-control'}),
            'parent': forms.TextInput(attrs = {'class': 'form-control'}),
            'observation': forms.Textarea(attrs = {'class': 'form-control'}),
        }