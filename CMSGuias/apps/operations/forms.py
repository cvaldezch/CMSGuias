#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django import forms

from .models import MetProject


class MetProjectForm(forms.ModelForm):
    class Meta:
        model = MetProject
        exclude = {'flag',}