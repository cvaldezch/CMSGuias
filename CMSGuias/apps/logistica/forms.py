# -*- coding: utf-8 -*-
from django  import forms
from .models import tmpcotizacion, tmpcompra

# tmpcotizacion
class addTmpCotizacionForm(forms.ModelForm):
    class Meta:
        model = tmpcotizacion
        exclude = {'empdni',}

# tmpcompra
class addTmpCompraForm(forms.ModelForm):
    class Meta:
        model = tmpcompra
        exclude = {'empdni',}