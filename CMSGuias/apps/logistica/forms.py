# -*- coding: utf-8 -*-
from django  import forms
from .models import tmpcotizacion

# tmpcotizacion
class addTmpCotizacionForm(forms.ModelForm):
    class Meta:
        model = tmpcotizacion
        exclude = {'empdni',}
