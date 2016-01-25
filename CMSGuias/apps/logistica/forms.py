# -*- coding: utf-8 -*-
from django import forms
from .models import tmpcotizacion, tmpcompra, Compra, ServiceOrder
from CMSGuias.apps.home.models import Proveedor


# tmpcotizacion
class addTmpCotizacionForm(forms.ModelForm):
    class Meta:
        model = tmpcotizacion
        exclude = {'empdni'}


# tmpcompra
class addTmpCompraForm(forms.ModelForm):
    class Meta:
        model = tmpcompra
        exclude = {'empdni', 'unit'}


# Purchase
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        exclude = {
            'compra_id',
            'registrado',
            'flag',
            'empdni',
            'status',
            'discount',
            'projects',
            'sigv'}


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        exclude = {'flag'}


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        exclude = {'serviceorder_id', 'elaborated', 'flag', 'status'}
