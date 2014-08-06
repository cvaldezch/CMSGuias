#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django import forms

from .models import MetProject
from CMSGuias.apps.almacen.models import tmpniple


class MetProjectForm(forms.ModelForm):
    class Meta:
        model = MetProject
        exclude = {'flag','tag',}

class tmpnipleForm(forms.ModelForm):
    class Meta:
        model = tmpniple
        exclude = {'flag','empdni',}