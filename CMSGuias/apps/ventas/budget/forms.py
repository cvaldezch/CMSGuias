#!/usr/bin/env python
#-*- Encoding: utf-8 -*-

from django import forms

from .models import *


class addAnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        exclude = {'analysis_id', 'flag',}

class addAnalysisGroupForm(forms.ModelForm):
    class Meta:
        model = AnalysisGroup
        exclude = {'agroup_id','regsiter', 'flag',}