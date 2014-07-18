#!/usr/bin/env python
#-*- Encoding: utf-8 -*-
#
from django import forms

from .models import Proyecto

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        exclude = {'proyecto_id','registrado','status','flag','empdni' }