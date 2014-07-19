#!/usr/bin/env python
#-*- Encoding: utf-8 -*-
#
from django import forms
from django.contrib.auth.models import User

from .models import Cliente


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
        EMPTY  = (("","Nothing"),)
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