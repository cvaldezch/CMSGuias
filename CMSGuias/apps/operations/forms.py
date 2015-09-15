#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django import forms

from .models import *
# from CMSGuias.apps.almacen.models import tmpniple


class MetProjectForm(forms.ModelForm):
    class Meta:
        model = MetProject
        exclude = {'flag', 'tag'}

# class tmpnipleForm(forms.ModelForm):
#     class Meta:
#         model = tmpniple
#         exclude = {'flag','empdni',}


class NippleForm(forms.ModelForm):
    class Meta:
        model = Nipple
        exclude = {'flag', 'tag'}


class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        exclude = {'letter_id', 'project', 'performed', 'status'}


class PreOrdersForm(forms.ModelForm):
    class Meta:
        model = PreOrders
        exclude = {
                    'preorder_id',
                    'performed',
                    'status',
                    'project',
                    'subproject',
                    'sector',
                    'flag',
                    'annular'}


class SGroupForm(forms.ModelForm):
    class Meta:
        model = SGroup
        exclude = {
            'project',
            'sector',
            'register',
            'datestart',
            'dateend',
            'flag'
        }
