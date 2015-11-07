#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django import forms

from CMSGuias.apps.home.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = {
            'flag',
            'register',
        }
