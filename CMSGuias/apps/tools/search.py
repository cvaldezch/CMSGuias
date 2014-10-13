#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

from CMSGuias.apps.home.models import Brand, Model

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
