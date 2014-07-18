#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from random import randint

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from CMSGuias.apps.almacen.models import Pedido, GuiaRemision, Suministro
from CMSGuias.apps.logistica.models import Cotizacion, Compra
from CMSGuias.apps.ventas.models import Proyecto


### format date str
__date_str = "%Y-%m-%d"
__year_str = "%y" # 'AA'
###


def __init__():
    return "MSG => select key generator"

def GenerateIdOrders():
    id = None
    try:
        cod = Pedido.objects.all().aggregate(Max('pedido_id'))
        id = cod['pedido_id__max']
        an= int(datetime.datetime.today().strftime(__year_str))
        if id is not None:
            aa= int(id[2:4])
            count = int(id[4:10])
            if an > aa:
                count = 1
            else:
                count+= 1
        else:
            count = 1
        id= "%s%s%s"%('PE',str(an),"{:0>6d}".format(count))
    except ObjectDoesNotExist, e:
        msg = "Error generator"
    return u"%s"%id
#generate serie - number of guide for key guide remision
def GenerateSerieGuideRemision():
    id = None
    try:
        cod= GuiaRemision.objects.all().aggregate(Max('guia_id'))
        id= cod['guia_id__max']
        if id is not None:
            #print 'codigo not empty'
            sr= int(id[0:3])
            num= int(id[4:])
            #print "%i %i"%(sr,num)
            sr= sr+1 if num >= 99999999 else sr
            num= num+1 if num <= 99999999 else 1
            #print "%i %i"%(sr,num)
        else:
            sr= 1
            num= 1
        id= "%s-%s"%("{:0>3d}".format(sr),"{:0>8d}".format(num))
    except ObjectDoesNotExist, e:
        id= "000-00000000"
    return id

# Generate id for order supply
def GenerateKeySupply():
    id = None
    try:
        cod = Suministro.objects.aggregate(max=Max('suministro_id'))
        id = cod['max']
        cy = int(datetime.datetime.today().strftime(__year_str))
        if id is not None:
            yy = int(id[2:4])
            counter = int(id[4:10])
            if cy > yy:
                counter = 1
            else:
                counter += 1
        else:
            counter = 1
        id = "%s%s%s"%('SP', cy.__str__(), "{:0>6d}".format(counter))
    except ObjectDoesNotExist:
      raise e
    return id

# Generate id for order Quotation
def GenerateKeyQuotation():
    id = None
    try:
        cod = Cotizacion.objects.aggregate(max=Max('cotizacion_id'))
        id = cod['max']
        cy = int(datetime.datetime.today().strftime(__year_str))
        if id is not None:
            yy = int(id[2:4])
            counter = int(id[4:10])
            if cy > yy:
                counter = 1
            else:
                counter += 1
        else:
            counter = 1
        id = "%s%s%s"%('SC', cy.__str__(), "{:0>6d}".format(counter))
    except ObjectDoesNotExist, e:
      raise e
    return id

def GeneratekeysQuoteClient():
    keys = ""
    try:
        chars = "aObAcPdB1Qe2Cf3Dg4Rh5Ei6S7jF8kT9lG0UmnHoWpIqJrYsKtLuZwMyzN-*!#^*()=_|"
        for x in xrange(1, 10):
            index = randint(0, (chars.__len__() - 1))
            keys = "%s%s"%(keys, chars[index])
    except Exception, e:
        raise e
    return "SC%s"%keys

# Generate id for order Quotation
def GenerateKeyPurchase():
    id = None
    try:
        cod = Compra.objects.aggregate(max=Max('compra_id'))
        id = cod['max']
        cy = int(datetime.datetime.today().strftime(__year_str))
        if id is not None:
            yy = int(id[2:4])
            counter = int(id[4:10])
            if cy > yy:
                counter = 1
            else:
                counter += 1
        else:
            counter = 1
        id = "%s%s%s"%('OC', cy.__str__(), "{:0>6d}".format(counter))
    except ObjectDoesNotExist:
      raise e
    return id

# Generate Id for Project
def GenerateIdPorject():
    id = None
    try:
        code = Proyecto.objects.aggregate(max=Max('proyecto_id'))
        id = code['max']
        yn = datetime.datetime.today().date().year
        if id is not None:
            yy = int(id[2:4])
            counter = int(id[4:7])
            if yn > yy:
                counter = 1
            else:
                counter += 1
        else:
            counter = 1
        id = '%s%s%s'%('PR',yn.__str__(), '{:0>3d}'.format(counter))
    except ObjectDoesNotExist, e:
        raise e
    return id