#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from random import randint

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from CMSGuias.apps.almacen.models import Pedido, GuiaRemision, Suministro, NoteIngress
from CMSGuias.apps.logistica.models import Cotizacion, Compra, ServiceOrder
from CMSGuias.apps.ventas.models import Proyecto
from CMSGuias.apps.home.models import Brand, Model, GroupMaterials, TypeGroup
from CMSGuias.apps.operations.models import Deductive, Letter, PreOrders
from CMSGuias.apps.ventas.budget.models import AnalysisGroup, Analysis

### format date str
__date_str = '%Y-%m-%d'
__year_str = '%y' # 'AA'
###


def __init__():
    return 'MSG => select key generator'

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
    keys = ''
    try:
        chars = '@ObAcPdB1Qe2Cf3Dg4Rh5Ei6S7jF8kT9lG0UmnHoWpIqJrYsKtLuZwMyzN!()=|'
        for x in xrange(1, 10):
            index = randint(0, (chars.__len__() - 1))
            keys = '%s%s'%(keys, chars[index])
    except Exception, e:
        raise e
    return 'SC%s'%keys

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
        yn = int(datetime.datetime.today().strftime(__year_str))
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

# Generate Id for Brand
def GenerateIdBrand():
    id = None
    try:
        code = Brand.objects.aggregate(max=Max('brand_id'))
        id = code['max']
        if id is not None:
            counter = int(id[2:5])
            counter += 1
        else:
            counter = 1
        id = '%s%s'%('BR', '{:0>3d}'.format(counter))
    except ObjectDoesNotExist, e:
        raise e
    return id

# Generate Id for Model
def GenerateIdModel():
    id = None
    try:
        code = Model.objects.aggregate(max=Max('model_id'))
        id = code['max']
        if id is not None:
            counter = int(id[2:5])
            counter += 1
        else:
            counter = 1
        id = '%s%s'%('MO', '{:0>3d}'.format(counter))
    except ObjectDoesNotExist, e:
        raise e
    return id

def GenerateIdNoteIngress():
    id = None
    try:
        code = NoteIngress.objects.aggregate(max=Max('ingress_id'))
        id = code['max']
        yn = int(datetime.datetime.today().strftime(__year_str))
        if id is not None:
            yy = int(id[2:4])
            counter = int(id[4:10])
            if yn > yy:
                counter = 1
            else:
                counter += 1
        else:
            counter = 1
        id = '%s%s%s'%('NI',yn.__str__(), '{:0>6d}'.format(counter))
    except ObjectDoesNotExist, e:
        raise e
    return id

def GenerateIdDeductive():
    id = None
    try:
        code = Deductive.objects.aggregate(max=Max('deductive_id'))
        id = code['max']
        yn = int(datetime.datetime.today().strftime(__year_str))
        if id is not None:
            yy = int(id[2:4])
            counter = int(id[4:10])
            if yn > yy:
                counter = 1
            else:
                counter += 1
        else:
            counter = 1
        id = '%s%s%s'%('DC', yn.__str__(), '{:0>6d}'.format(counter))
    except ObjectDoesNotExist, e:
        raise e
    return id

def GenerateIdGroupMaterials():
    id = None
    try:
        code = GroupMaterials.objects.aggregate(max=Max('mgroup_id'))
        id = code['max']
        if id is not None:
            counter = int(id[2:10])
            counter += 1
        else:
            counter = 1
        id = '%s%s'%('GM', '{:0>8d}'.format(counter))
    except ObjectDoesNotExist, e:
        raise e
    return id

def GenerateIdTypeGroupMaterials():
    id = None
    try:
        code = TypeGroup.objects.aggregate(max=Max('tgroup_id'))
        id = code['max']
        if id is not None:
            counter = int(id[2:7])
            counter += 1
        else:
            counter = 1
        id = '%s%s'%('TG', '{:0>5d}'.format(counter))
    except ObjectDoesNotExist, e:
        raise e
    return id

# Generate Key COnfirm
def GeneratekeysConfirm():
    keys = ''
    try:
        chars = '1234567890'
        for x in xrange(0, 6):
            index = randint(0, (chars.__len__() - 1))
            keys = '%s%s'%(keys, chars[index])
    except Exception, e:
        raise e
    return '%s'%keys

def GenerateIdServiceOrder():
    id = None
    try:
        code = ServiceOrder.objects.aggregate(max=Max('serviceorder_id'))
        id = code['max']
        yn = int(datetime.datetime.today().strftime(__year_str))
        if id is not None:
            yy = int(id[2:4])
            counter = int(id[4:10])
            if yn > yy:
                counter = 1
            else:
                counter += 1
        else:
            counter = 1
        id = '%s%s%s'%('SO',yn.__str__(), '{:0>6d}'.format(counter))
    except ObjectDoesNotExist, e:
        raise e
    return id

def generateLetterCode(pro='PRAA000', ruc = ''):
    id = None
    try:
        code = Letter.objects.latest('register')
        # print code.register
        id = code.letter_id
        yn = int(datetime.datetime.today().strftime(__year_str))
        if id is not None:
            counter = int(id[-3:])
            if yn > int(code.register.strftime('%y')):
                counter = 1
            else:
                counter += 1
        else:
            counter = 1
        if ruc == '20428776110':
            signal = 'ICR'
        else:
            signal = 'ICT'
        id = 'CTA-%s-%s-%s'%(signal, pro,'{:0>3d}'.format(counter))
    except ObjectDoesNotExist, e:
        id = 'CTA-%s-%s-%s'%('ICR', pro,'{:0>3d}'.format(1))
    return id

def generatePreOrdersId():
    id = None
    yn = int(datetime.datetime.today().strftime(__year_str))
    try:
        code = PreOrders.objects.latest('register')
        id = code.preorder_id
        if id is not None:
            yy = int(id[3:5])
            counter = int(id[5:10])
            if yn > yy:
                counter = 1
            else:
                counter += 1
        else:
            counter = 1
        id = '%s%i%s'%('PRO',yn, '{:0>5d}'.format(counter))
    except ObjectDoesNotExist, e:
        id = '%s%i%s'%('PRO',yn, '{:0>5d}'.format(1))
    return id

def generateAnalysis():
    id = None
    try:
        code = Analysis.objects.latest('register')
        id = code.analysis_id
        if code.analysis_id:
            counter = int(code.analysis_id[2:])
            counter += 1
        else:
            counter = 1
        id = '%s%s'%('AP', '{:0>6d}'.format(counter))
    except ObjectDoesNotExist, e:
        id = '%s%s'%('AP', '{:0>6d}'.format(1))
    return id

def generateGroupAnalysis():
    id = None
    try:
        code = AnalysisGroup.objects.latest('register')
        if code.agroup_id:
            counter = int(code.agroup_id[2:])
            counter += 1
        else:
            counter = 1
        id = '%s%s'%('AG', '{:0>3d}'.format(counter))
    except ObjectDoesNotExist, e:
        id = '%s%s'%('AG', '{:0>3d}'.format(1))
    return id