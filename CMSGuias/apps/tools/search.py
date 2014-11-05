#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

from CMSGuias.apps.home.models import Brand, Model, Configuracion
from CMSGuias.apps.ventas.models import *
from CMSGuias.apps.tools import globalVariable

class searchBrands:
    """docstring for searchBrands"""

    brand = ""

    def validFormat(self):
        if self.brand.strip() == "":
            return False
        else:
            self.brand = self.brand.strip()
            return True

    def autoDetected(self):
        print self.brand[:2]
        if self.brand[:2] == "BR":
            try:
                #obj = Brand.objects.get(pk=self.brand)
                return dict((('pk',self.brand),))
            except ObjectDoesNotExist, e:
                raise e
        else:
            obj = Brand.objects.filter(brand__istartswith=self.brand.lower())[:1]
            print obj
            return dict((('pk',obj[0].brand_id),))

class searchModels:
    """docstring for searchModels"""

    model = ""

    def validFormat(self):
        if self.model.strip() == "":
            return False
        else:
            self.model = self.model.strip()
            return True

    def autoDetected(self):
        if self.model[:2] == "MO":
            try:
                #obj = model.objects.get(pk=self.model)
                return dict((('pk',self.model),))
            except ObjectDoesNotExist, e:
                raise e
        else:
            obj = Model.objects.filter(model__istartswith=self.model.lower())[:1]
            print obj
            return dict((('pk',obj[0].model_id),))

## Get period of project
def searchPeriodProject(code=''):
    period = ''
    if code == '':
        period = globalVariable.get_year
    else:
        try:
            period = Proyecto.objects.get(proyecto_id)
            period = period.registrado.strftime('%Y')
        except ObjectDoesNotExist, e:
            period = globalVariable.get_year
    return period

# Get igv for year current
def getigvCurrent():
    igv = ''
    try:
        igv = Configuracion.objects.get(periodo__exact=globalVariable.get_year)
        igv = igv.igv
    except ObjectDoesNotExist, e:
        raise e
    return igv