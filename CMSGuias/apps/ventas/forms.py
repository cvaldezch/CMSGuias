#!/usr/bin/env python
#-*- Encoding: utf-8 -*-
#
from django import forms

from .models import Proyecto, Sectore, Subproyecto, SectorFiles, Metradoventa, Alertasproyecto, PurchaseOrder

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        exclude = {'proyecto_id','registrado','status','flag','empdni' }

class SectoreForm(forms.ModelForm):
    class Meta:
        model = Sectore
        exclude = {'registrado', 'status', 'flag',}
        atypel = (
                    ('NN','NOTHING'),
                    ('GL','GLOBAL'),
                    ('LC','SECTOR'),
                    ('PE','PERSONALIZADO'),
                )
        widgets = {
            'sector_id' : forms.TextInput(attrs = {'class':'form-control','maxlength': '13'}),
            'proyecto' : forms.TextInput(attrs = {'class':'form-control', 'readonly':'readonly'}),
            'subproyecto' : forms.TextInput(attrs = {'class':'form-control', 'readonly':'readonly'}),
            'planoid' : forms.TextInput(attrs = {'class':'form-control'}),
            'nomsec' : forms.TextInput(attrs = {'class':'form-control'}),
            'comienzo' : forms.TextInput(attrs = {'class':'form-control'}),
            'fin' : forms.TextInput(attrs = {'class':'form-control'}),
            'obser' : forms.Textarea(attrs = {'class': 'form-control', 'maxlength': '200', 'rows': '4'}),
            'amount' : forms.TextInput(attrs = {'class':'form-control'}),
            'atype' : forms.Select(attrs = {'class':'form-control'}, choices=atypel),
        }

class SubprojectForm(forms.ModelForm):
    class Meta:
        model   = Subproyecto
        exclude = {'registrado', 'status','flag',}
        widgets = {
            'subproyecto_id' : forms.TextInput(attrs ={'class':'form-control'}),
            'nomsub': forms.TextInput(attrs = {'class': 'form-control'}),
            'comienzo': forms.TextInput(attrs ={'class': 'form-control in-date','maxlength':'10','placeholder':'aaaa-mm-dd'}),
            'fin': forms.TextInput(attrs ={'class': 'form-control in-date','maxlength':'10','placeholder':'aaaa-mm-dd'}),
            'obser': forms.Textarea(attrs ={'class': 'form-control', 'maxlength':'200','rows':'3'}),
        }

class SectorFilesForm(forms.ModelForm):
    class Meta:
        model = SectorFiles
        exclude = {'flag',}

class MetradoventaForm(forms.ModelForm):
    class Meta:
        model = Metradoventa
        exclude = {'flag',}

class AlertasproyectoForm(forms.ModelForm):
    class Meta:
        model = Alertasproyecto
        exclude = {'registrado', 'empdni', 'charge', 'flag',}

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        exclude = {'id','project','flag',}