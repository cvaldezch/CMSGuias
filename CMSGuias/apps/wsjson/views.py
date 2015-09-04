# -*- coding: utf-8 -*-
import csv
import json
import datetime
import urllib2
import re
from bs4 import BeautifulSoup

# from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
# from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View

from CMSGuias.apps.almacen.models import *
from CMSGuias.apps.home.models import *
from CMSGuias.apps.ventas.models import (
        Proyecto, Sectore, Subproyecto, Metradoventa)
from CMSGuias.apps.operations.models import MetProject
from CMSGuias.apps.tools import uploadFiles, globalVariable, search, genkeys


class JSONResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            mimetype='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        return simplejson.dumps(context, encoding='utf-8')


def get_description_materials(request):
    context = dict()
    if request.method == 'GET':
        try:
            name = Materiale.objects.values('matnom').filter(
                    matnom__icontains=request.GET.get('nom')
                    ).distinct('matnom').order_by('matnom')
            context['name'] = [{'matnom': x['matnom']} for x in name]
            context['status'] = True
        except ObjectDoesNotExist:
            context['status'] = False
        return HttpResponse(
                simplejson.dumps(context),
                mimetype='application/json')
    # try:
    #     if request.method == 'GET':
    #         try:
    #             data = {'name':[]}
    #             name = Materiale.objects.values('matnom').filter(matnom__icontains=request.GET['nom']).distinct('matnom').order_by('matnom')
    #             i = 0
    #             for x in name:
    #                 data['name'].append({'matnom':x['matnom'],'id':i})
    #                 i += 1
    #         except ObjectDoesNotExist, e:
    #             raise e
    #         return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    # except ObjectDoesNotExist:
    #     raise Http404


def get_meter_materials(request):
    if request.method == 'GET':
        context = {}
        try:
            meter = Materiale.objects.values('materiales_id', 'matmed').filter(
                    matnom__exact=request.GET['matnom']).order_by('matmed')
            context['list'] = [{
                'materiales_id': x['materiales_id'],
                'matmed': x['matmed']}
                for x in meter]
            context['status'] = True
        except ObjectDoesNotExist:
            context['status'] = False
        return JSONResponseMixin().render_to_json_response(context)
    # try:
    #     if request.method == 'GET':
    #         data = { "list": [] }
    #         meter = Materiale.objects.values('matmed').filter(matnom__contains=request.GET['matnom']).distinct('matnom','matmed').order_by('matmed')
    #         for x in meter:
    #             data["list"].append({ "matmed": x["matmed"] })
    #         return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    # except ObjectDoesNotExist:
    #     raise Http404


def get_resumen_details_materiales(request):
        if request.method == 'GET':
            context = dict()
            try:
                summ = Materiale.objects.filter(
                        materiales_id=request.GET['matid'])
                # matmed__icontains=request.GET.get('matmed'))
                for x in summ:
                    if x.materiales_id == request.GET['matid']:
                        purchase, sale, quantity = 0, 0, 0
                        if 'pro' in request.GET:
                            name = 'PRICES%s' % (request.GET.get('pro'))
                            if name in request.session:
                                sectors = request.session[name]
                                for s in sectors:
                                    if request.GET.get('sec') in s:
                                        for p in s[request.GET.get('sec')]:
                                            condition = (
                                                        x.materiales_id ==
                                                        p['materials']
                                                        )
                                            if condition:
                                                purchase = round(
                                                            p['purchase'], 2)
                                                sale = round(p['sale'], 2)
                                                quantity = p['quantity']
                            else:
                                try:
                                    getprices = MetProject.objects.filter(materiales_id=x.materiales_id).distinct('proyecto__proyecto_id').order_by('proyecto__proyecto_id').reverse()
                                    if getprices:
                                        getprices = getprices[0]
                                        purchase = getprices.precio
                                        # max([p.precio for p in getprices])
                                        sale = getprices.sales
                                        # max([p.sales for p in getprices])
                                    else:
                                        purchase = 0
                                        sale = 0
                                except ObjectDoesNotExist, e:
                                    purchase = 0
                                    sale = 0

                        context['list'] = [
                            {
                                'materialesid': x.materiales_id,
                                'matnom': x.matnom,
                                'matmed': x.matmed,
                                'unidad': x.unidad.uninom,
                                'purchase': purchase,
                                'sale': float(sale),
                                'quantity': quantity
                            }
                        ]
                        break
                context['status'] = True
            except ObjectDoesNotExist:
                context['raise'] = e.__str__()
                context['status'] = False
            return HttpResponse(simplejson.dumps(context),
                                mimetype='application/json')


class SearchBrand(JSONResponseMixin, DetailView):
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            context['brand'] = [{'brand_id': x.brand_id, 'brand': x.brand} for x in Brand.objects.filter(flag=True).order_by('brand')]
            context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return self.render_to_json_response(context)

class SearchModel(JSONResponseMixin, DetailView):
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            context['model'] = [{'model_id': x.model_id, 'model': x.model} for x in Model.objects.filter(flag=True).order_by('model')]
            context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return self.render_to_json_response(context)

class GetDetailsMaterialesByCode(DetailView):
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                mat = Materiale.objects.values(
                        'materiales_id', 'matnom', 'matmed', 'unidad').get(
                        pk=request.GET.get('code'))
                purchase, sale, quantity = 0, 0, 0
                if 'pro' in request.GET:
                    name = 'PRICES%s' % (request.GET.get('pro'))
                    if name in request.session:
                        sectors = request.session[name]
                        for s in sectors:
                            if request.GET.get('sec') in s:
                                for p in s[request.GET.get('sec')]:
                                    if mat['materiales_id'] == p['materials']:
                                        purchase = round(p['purchase'], 2)
                                        sale = round(p['sale'], 2)
                                        quantity = p['quantity']
                    else:
                        try:
                            getprices = MetProject.objects.filter(materiales_id=mat['materiales_id']).distinct('proyecto__proyecto_id').order_by('proyecto__proyecto_id').reverse()
                            if getprices:
                                getprices = getprices[0]
                                purchase = getprices.precio
                                # max([p.precio for p in getprices])
                                sale = getprices.sales
                                # max([p.sales for p in getprices])
                            else:
                                purchase = 0
                                sale = 0
                        except ObjectDoesNotExist, e:
                            purchase = 0
                            sale = 0
                context['list'] = {
                    'materialesid': mat['materiales_id'],
                    'matnom': mat['matnom'],
                    'matmed': mat['matmed'],
                    'unidad': mat['unidad'],
                    'purchase': purchase,
                    'sale': float(sale),
                    'quantity': quantity
                }
                context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = str(e)
                context['status'] = False
            return HttpResponse(simplejson.dumps(context),
                                mimetype='application/json')

def save_order_temp_materials(request):
    data = dict()
    if request.method == 'POST':
        try:
            c = tmppedido.objects.get(empdni__exact=request.user.get_profile().empdni_id,materiales_id__exact=request.POST['mid'])
            c.cantidad += float(request.POST.get('cant'))
            c.brand_id = request.POST.get('brand')
            c.model_id = request.POST.get('model')
            c.save()
        except ObjectDoesNotExist:
            obj = tmppedido()
            obj.empdni = request.user.get_profile().empdni_id
            obj.materiales_id = request.POST.get('mid')
            obj.cantidad = float(request.POST.get('cant'))
            obj.brand_id = request.POST.get('brand')
            obj.model_id = request.POST.get('model')
            obj.save()
        if 'details' in request.POST:
            for x in json.loads(request.POST.get('details')):
                try:
                    c = tmppedido.objects.get(empdni__exact=request.user.get_profile().empdni_id,materiales_id__exact=x['materials'])
                    c.cantidad += (float(x['quantity']) * float(request.POST.get('cant')))
                    c.save()
                except ObjectDoesNotExist:
                    obj = tmppedido()
                    obj.empdni = request.user.get_profile().empdni_id
                    obj.materiales_id = x['materials']
                    obj.cantidad = (float(x['quantity']) * float(request.POST.get('cant')))
                    obj.brand_id = 'BR000'
                    obj.model_id = 'MO000'
                    obj.save()
        data['status'] = True
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def update_order_temp_materials(request):
    try:
        data = dict()
        if request.method == "POST":
            obj = tmppedido.objects.get(empdni__exact=request.user.get_profile().empdni_id,materiales_id__exact=request.POST['mid'])
            obj.cantidad = request.POST.get('cantidad')
            obj.brand_id = request.POST.get('brand')
            obj.model_id = request.POST.get('model')
            obj.save()
            data['status'] = True
    except ObjectDoesNotExist, e:
        data['status'] = False
        data['raise'] = e.__str__()
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def delete_order_temp_material(request):
    try:
        data = {}
        if request.method == "POST":
            obj = tmppedido.objects.get(empdni__exact=request.POST['dni'],materiales_id__exact=request.POST['mid'])
            obj.delete()
            data['status'] = True
        else:
            data['status'] = False
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    except ObjectDoesNotExist, e:
        raise e

def delete_all_temp_order(request):
    try:
        data = {}
        if request.method == "POST":
            # get objects to delete; these are of table bedside
            obj = tmppedido.objects.filter(empdni__exact=request.POST['dni'])
            obj.delete()
            # here get object "Niples" tambien deberan ser eliminadas
            tmp = tmpniple.objects.filter(empdni__exact=request.POST.get('dni'))
            tmp.delete()
            data['status'] = True
        else:
            data['status'] = False
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    except ObjectDoesNotExist, e:
        raise e

def get_list_order_temp(request):
    try:
        data = {'list':[]}
        if request.method == 'GET':
            ls = tmppedido.objects.filter(empdni__startswith=request.user.get_profile().empdni_id).order_by('materiales__matnom')
            #lista = [ {"cant": x.cantidad, "materiales_id": x.materiales_id, "matnom": x.materiales.matnom } for x in ls ]
            counter = 1
            for x in ls:
                data['list'].append(
                    {
                        'item': counter,
                        'materiales_id': x.materiales_id,
                        'matnom': x.materiales.matnom,
                        'matmed': x.materiales.matmed,
                        'brand': x.brand.brand,
                        'model': x.model.model,
                        'unidad': x.materiales.unidad.uninom,
                        'cantidad': x.cantidad
                    }
                )
                counter+=1
            data['status'] = True
        else:
            data['status'] = False
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    except ObjectDoesNotExist, e:
        raise e

def get_details_materials_by_id(request):
    try:
        data = {}
        if request.method == 'GET':
            mat = Materiale.objects.values('materiales_id','matnom','matmed','unidad_id').get(pk=request.GET.get('mid'))
            if len(mat) > 0:
                mat['status'] = True
            return HttpResponse(simplejson.dumps(mat),mimetype='application/json')
    except ObjectDoesNotExist, e:
        raise e
# sending list of nipples
def get_list_beside_nipples_temp_orders(request):
    try:
        data = {}
        if request.method == 'GET':
            ls = tmppedido.objects.filter(materiales__materiales_id__startswith='115').order_by("materiales")
            if len(ls) > 0:
                data['status'] = True
                data['nipples'] = [ {"materiales_id":x.materiales.materiales_id,"matnom":x.materiales.matnom,"matmed":x.materiales.matmed,"unidad":x.materiales.unidad_id, "cantidad": x.cantidad } for x in ls]
            else:
                data['status'] = False
                data['niples'] = "Nothing"
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    except ObjectDoesNotExist, e:
        raise e
# list temp nipples
def get_list_temp_nipples(request):
    try:
        data = {}
        if request.method == 'GET':
            tipo = {'A':"Roscado","B":"Ranurado", "C":"Roscado - Ranurado" }
            ls = tmpniple.objects.filter(empdni__exact=request.GET['dni'],materiales_id__exact=request.GET['mid']).order_by('metrado')
            data['list'] = [ { "id": x.id,"cantidad":x.cantidad,"materiales_id":x.materiales.materiales_id,"matnom": 'Niple '+tipo[x.tipo],"matmed":x.materiales.matmed, "metrado": x.metrado, "tipo": x.tipo } for x in ls]
            data['status'] = True
        else:
            data['status'] = False
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    except ObjectDoesNotExist:
        raise Http404
# saved or update templates nipples
def post_saved_update_temp_nipples(request):
    data = {}
    if request.method == 'POST':
        try:
            if request.POST.get('tra') == 'new':
                obj = tmpniple()
            else:
                obj = tmpniple.objects.get(id=request.POST.get('id'))
            obj.empdni = request.POST.get('dni')
            obj.materiales_id = request.POST.get('mid')
            obj.cantidad = request.POST.get('veces')
            obj.metrado = request.POST.get('cant')
            obj.tipo = request.POST.get('type')
            obj.save()
            data['status'] = True
        except ObjectDoesNotExist, e:
            raise e
            data['status'] = False
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
# delete item nipple template
def post_delete_temp_item_nipple(request):
    data = {}
    if request.method == 'POST':
        try:
            obj = tmpniple.objects.get(id__exact=request.POST.get('id'), materiales_id__exact=request.POST.get('mid'),empdni__exact=request.POST.get('dni'))
            obj.delete()
            data['status'] = True
        except ObjectDoesNotExist, e:
            raise e
            data['status'] = False
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
# delete item nipple template
def post_delete_temp_all_nipple(request):
    data = {}
    if request.method == 'POST':
        try:
            obj = tmpniple.objects.filter(materiales_id__exact=request.POST.get('mid'))
            obj.delete()
            data['status'] = True
        except ObjectDoesNotExist, e:
            raise e
            data['status'] = False
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
## upload file orders temp and reader file temp orders
@login_required(login_url='/SignUp/')
def post_upload_file_temp_orders(request):
    data= {}
    if request.method == 'POST':
        if request.is_ajax():
            from CMSGuias.apps.tools import uploadFiles
            from xlrd import open_workbook, XL_CELL_EMPTY
            try:
                # upload file
                arch= request.FILES['ftxls']
                filename= uploadFiles.upload('/storage/temporary/',arch)
                # read file
                book= open_workbook(filename,encoding_override='utf-8')
                sheet= book.sheet_by_index(0) # recover sheet of materials
                arn= [] # array list of materials to nipples
                # retrive the values of the first sheet
                for m in range(10, sheet.nrows):
                    mid= sheet.cell(m, 2)
                    # conditions for get rows values
                    if mid.ctype!=XL_CELL_EMPTY: # cell different to empty or blank
                        mid= str(int(mid.value))
                        if len(mid) == 15: # row code is length equal 15 chars
                            arn.append(mid) if mid[0:3] == '115' else False # aggregate materials for nipples
                            cant= sheet.cell(m, 6) # get quantity
                            obj, created= tmppedido.objects.get_or_create(materiales_id=mid,empdni=request.user.get_profile().empdni_id,defaults={'cantidad':cant.value})
                            if not created:
                                obj.cantidad= (obj.cantidad + cant.value)
                                obj.save()
                if len(arn) > 0:
                    sheet= book.sheet_by_index(1) # recover sheet of nipples
                    for n in range(9, sheet.nrows):
                        mid = sheet.cell(n, 2)
                        if mid.ctype != XL_CELL_EMPTY: # cell different to empty
                            mid= str(int(mid.value)) # convert cell value to str
                            if mid in arn:
                                # values other columns
                                cant= sheet.cell(n, 3).value # quantity of nipples
                                med= sheet.cell(n, 7).value # meter in cm
                                tipo= sheet.cell(n, 5).value # type nipple {A, B, C}
                                # create or update nipples
                                obj, created= tmpniple.objects.get_or_create(materiales_id=mid,metrado=med,tipo=tipo,empdni=request.user.get_profile().empdni_id,defaults={'cantidad':cant})
                                if not created:
                                    obj.cantidad= ( obj.cantidad + cant )
                                    obj.save()
                            else:
                                continue
                uploadFiles.removeTmp(filename) # remove temp file
                data['status']= True
            except Exception, e:
                data['status']= False
            #print 'Num Rows: %i'%sheet.nrows
            return HttpResponse(simplejson.dumps(data),mimetype="application/json")
###
"""
##    Recurrent get list
"""
# get list of Projects
def get_list_projects(request):
    if request.method == 'GET':
        data = {}
        try:
            lst = Proyecto.objects.values('proyecto_id','nompro').filter(flag=True,status='AC')
            data['list'] = [ { "proyecto_id": x['proyecto_id'], "nompro":x['nompro'] } for x in lst ]
            data['status'] = True
        except Exception, e:
            data['status'] = False
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
# get list sectors
def get_list_sectors(request):
    if request.method == 'GET':
        data = {}
        try:
            if "sub" in request.GET:
                lst = Sectore.objects.values('sector_id','planoid','nomsec').filter(proyecto_id=request.GET.get('pro'),subproyecto_id=request.GET.get('sub'))
            else:
                lst = Sectore.objects.values('sector_id','planoid','nomsec').filter(proyecto_id=request.GET.get('pro'),subproyecto_id=None)
            data['list']= [ { "sector_id":x['sector_id'], "planoid":x['planoid'], "nomsec":x['nomsec'] } for x in lst ]
            data['status']= True
        except ObjectDoesNotExist, e:
            data['status'] = False
        return HttpResponse(simplejson.dumps(data),mimetype="application/json")
# get list subprojects
def get_list_subprojects(request):
    if request.method == 'GET':
        data = {}
        try:
            lst = Subproyecto.objects.values('subproyecto_id','nomsub').filter(proyecto_id=request.GET.get('pro'))
            data['list']= [ { "subproyecto_id":x['subproyecto_id'],"nomsub":x['nomsub'] } for x in lst ]
            data['status']= True
        except ObjectDoesNotExist, e:
            data['status']= False
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
# get list Stores
def get_list_stores(request):
    if request.method == 'GET':
        data = {}
        try:
            lst = Almacene.objects.values('almacen_id','nombre').filter(flag=True)
            data['list']= [ { 'almacen_id':x['almacen_id'], 'nombre': x['nombre'] } for x in lst ]
            data['status']= True
        except ObjectDoesNotExist, e:
            data['status']= False
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')

"""
## end block Recurrent
"""
# approve orders
def post_approved_orders(request):
    if request.method == 'POST':
        data = {}
        try:
            obj = Pedido.objects.get(pk=request.POST.get('oid'))
            obj.status = 'AP'
            obj.flag = True
            obj.save()
            data['status']= True
        except ObjectDoesNotExist, e:
            data['status']= False
            data['msg']= e
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# cancel orders
def post_cancel_orders(request):
    if request.method == 'POST':
        data = {}
        try:
            obj = Pedido.objects.get(pedido_id=request.POST.get('oid'))
            try:
                det = Detpedido.objects.filter(pedido_id=request.POST.get('oid'))
                for x in det:
                    meter = MetProject.objects.get(proyecto_id=obj.proyecto_id, subproyecto_id=obj.subproyecto_id, sector_id=obj.sector_id, materiales_id=x.materiales_id, brand_id=x.brand_id, model_id=x.model_id)
                    quantitydev = (x.cantidad + meter.quantityorder)
                    if quantitydev == meter.cantidad:
                        meter.tag = '0'
                        meter.quantityorder = quantitydev
                    if meter.quantityorder > 0 and quantitydev < meter.cantidad:
                        meter.tag = '1'
                        meter.quantityorder = quantitydev
                    if quantitydev > meter.cantidad:
                        meter.tag = '0'
                        meter.quantityorder = meter.cantidad
                    meter.quantityorder = quantitydev
                    meter.save()
                    x.tag = '3'
                    x.flag = False
                    x.save()
            except ObjectDoesNotExist, e:
                data['raise'] = str(e)
            obj.status = 'AN'
            obj.flag = False
            obj.save()
            data['status']= True
        except ObjectDoesNotExist, e:
            data['status']= False
            data['msg']= e.__str__()
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# recover list transport
def get_recover_list_transport(request,truc):
    if request.method == 'GET':
        if request.is_ajax():
            data= {}
            try:
                data['list']= [ {'nropla_id':x['nropla_id'],'marca':x['marca']} for x in Transporte.objects.values('nropla_id','marca').filter(traruc_id__exact=truc,flag=True) ]
                data['status']= True
            except ObjectDoesNotExist, e:
                data['status']= False
            return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# recover list conductor
def get_recover_list_conductor(request,truc):
    if request.method == 'GET':
        if request.is_ajax():
            data= {}
            try:
                data['list']= [ {'condni_id':x['condni_id'],'connom':x['connom'],'conlic':x['conlic']} for x in Conductore.objects.values('condni_id','connom','conlic').filter(traruc_id__exact=truc,flag=True) ]
                data['status']= True
            except ObjectDoesNotExist, e:
                data['status']= False
            return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# Class Views Generics
#
class get_OrdersDetails(ListView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
          context = {}
          try:
              arr = json.loads(request.GET.get('orders'))
              queryset = Detpedido.objects.filter(pedido_id__in=arr).extra(select = { 'stock': "SELECT stock FROM almacen_inventario WHERE almacen_detpedido.materiales_id LIKE almacen_inventario.materiales_id AND periodo LIKE to_char(now(), 'YYYY')"},)
              queryset = queryset.values('materiales_id','materiales__matnom','materiales__matmed','materiales__unidad_id','stock','spptag')
              queryset = queryset.annotate(cantidad=Sum('cantshop'))
              context['list'] = [{'materiales_id': x['materiales_id'],'matnom': x['materiales__matnom'],'matmed':x['materiales__matmed'],'unidad':x['materiales__unidad_id'],'cantidad':x['cantidad'],'stock':x['stock'],'tag':x['spptag']} for x in queryset]
              context['status'] = True
          except ObjectDoesNotExist:
              context['status'] = False
          return HttpResponse(simplejson.dumps(context),mimetype='application/json')

class SupplyDetailView(DetailView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            response = HttpResponse()
            response['content-type'] = 'application/json'
            response['mimetype'] = 'application/json'
            queryset = DetSuministro.objects.filter(suministro_id__exact=kwargs['sid'], flag=True)
            queryset = queryset.values('materiales_id','materiales__matnom','materiales__matmed','materiales__unidad__uninom','brand__brand','model__model','brand_id','model_id')
            queryset = queryset.annotate(cantidad=Sum('cantshop')).order_by('materiales__matnom')
            context['list'] = [
                {
                    'materiales_id': x['materiales_id'],
                    'materiales__matnom': x['materiales__matnom'],
                    'materiales__matmed': x['materiales__matmed'],
                    'materiales__unit': x['materiales__unidad__uninom'],
                    'brand': x['brand__brand'],
                    'model': x['model__model'],
                    'brand_id': x['brand_id'],
                    'model_id': x['model_id'],
                    'cantidad': x['cantidad']
                } for x in queryset
            ]
            bedside = Suministro.objects.get(pk=kwargs['sid'])
            context['project'] = [{'nompro': x.nompro} for x in Proyecto.objects.filter(proyecto_id__in=bedside.orders.split(','))]
            context['status'] = True
            response.write(simplejson.dumps(context))
        except ObjectDoesNotExist, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return response

class getSupplierList(JSONResponseMixin, DetailView):

    def get(self, rquest, *args, **kwargs):
        context = dict()
        try:
            supplier = Proveedor.objects.filter(flag=True).order_by('razonsocial')
            context['supplier'] = [{"supplier_id":x.proveedor_id, "company":x.razonsocial, "address":x.direccion,"phone":x.telefono,"type":x.tipo, "mail":x.email} for x in supplier]
            context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = e
            context['status'] = False
        return self.render_to_json_response(context, **kwargs)

class getStoreList(JSONResponseMixin, DetailView):

    def get(self, rquest, *args, **kwargs):
        context = dict()
        try:
            store = Almacene.objects.filter(flag=True).order_by('nombre')
            context['store'] = [{"store_id":x.almacen_id, "name":x.nombre} for x in store]
            context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = e
            context['status'] = False
        return self.render_to_json_response(context, **kwargs)

###
# Get data Sunat
# Solo habilitado para el tipo de cambio en Dolares Americanos
class RestfulExchangeRate(JSONResponseMixin, DetailView):
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            # Get exchange rate today
            date = datetime.datetime.today().date()
            currency = Configuracion.objects.get(periodo=date.year.__str__())
            exchange = TipoCambio.objects.filter(fecha=date, moneda_id=currency.moneda_id)
            if exchange.__len__() == 0:
                url = 'http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias'
                data = parseSunat(url)
                if data != 'Nothing':
                    soup = BeautifulSoup('"""%s"""'%data)
                    html = soup.select('body > form > div > center > table > tbody')
                    rate = html[1].find_all('td')
                    length = rate.__len__()
                    obj = TipoCambio()
                    obj.moneda_id = currency.moneda_id
                    purchase = float(re.sub('[(\n)(\t)(\s)]','',rate[length - 2].contents[0].string))
                    sale = float(re.sub('[(\n)(\t)(\s)]','',rate[length - 1].contents[0].string))
                    if currency.moneda.moneda.startswith('DOLARES'):
                        obj.compra = (1 / purchase)
                        obj.venta = (1 / sale)
                    else:
                        obj.compra = purchase
                        obj.venta = sale
                    obj.save()
                    day = int(rate[length - 3].strong.string)
                    if day != date.day:
                        context['rasie'] = 'the exchange rate, does not belong to the date.'
                    else:
                        context['raise'] = 'Successfully save.'
                    context['status'] = True
                else:
                    context['status'] = False
            else:
                context['raise'] = 'The exchange rate already this registered.'
                context['status'] = True
                context['show'] = False
        except Exception, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return self.render_to_json_response(context, **kwargs)

class RestfulDataRuc(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                url = 'http://www.sunat.gob.pe/w/wapS01Alias?ruc=%s'%(request.POST.get('ruc'))
                ruc = request.POST.get('ruc')
                #capcha = request.POST.get('capcha')
                #url = 'http://www.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorRuc&nroRuc=%s&tQuery=on&search1=%s&tipdoc=1&codigo=MHNH'%(ruc,ruc)
                data = parseSunat(url)
                print data
                if data != 'Nothing':
                    soup = BeautifulSoup(data)
                    for x in soup.find_all('small'):
                        tag = BeautifulSoup(x.__str__())
                        #print tag
                        conditional = tag.body.small.contents[0].string
                        if conditional.endswith('Ruc. '):
                            res = tag.body.small.contents[1]
                            res = res.split('-',1)
                            context['ruc'] = res[0].strip()
                            context['reason'] = res[1].strip()
                        if conditional.startswith('Direcci'):
                            context['address'] = tag.body.small.contents[2].string
                        if conditional.startswith('Tipo.'):
                            context['type'] = tag.body.small.contents[2]
                        if conditional.startswith('Tel'):
                            context['phone'] = tag.body.small.contents[2]
                        if conditional.startswith('DNI'):
                            context['dni'] = tag.body.small.contents[1].string[3:]
                        context['status'] = True
                    #print soup
                    context['status'] = True
                else:
                    context['status'] = False
            except Exception, e:
                contet['status'] = False
            return self.render_to_json_response(context)

def parseSunat(url):
    try:
        proxy = urllib2.ProxyHandler({'http': '172.16.0.1:8080'})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        return urllib2.urlopen(req).read()
    except Exception:
        return 'Nothing'

# stage2dev
# Country
class ViewContry(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if request.GET.get('type') == 'option':
                    context['country'] = [{'country_id': x.pais_id,'country':x.paisnom} for x in Pais.objects.filter(flag=True)]
                context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

class ViewDepartament(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if request.GET.get('type') == 'option':
                    context['departament'] = [{'departament_id': x.departamento_id, 'departament': x.depnom} for x in Departamento.objects.filter(pais_id=request.GET.get('country'), flag=True)]
                context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

class ViewProvince(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if request.GET.get('type') == 'option':
                    context['province'] = [{'province_id':x.provincia_id, 'province': x.pronom} for x in Provincia.objects.filter(pais_id=request.GET.get('country'), departamento_id=request.GET.get('departament'), flag=True)]
                context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

class ViewDistrict(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if request.GET.get('type') == 'option':
                    context['district'] = [{'district_id': x.distrito_id, 'district': x.distnom} for x in Distrito.objects.filter(pais_id=request.GET.get('country'), departamento_id=request.GET.get('departament'), provincia_id=request.GET.get('province'), flag=True)]
                context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

class ViewCopyMaterialesProjectsSale(JSONResponseMixin, DetailView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if 'project' in request.GET:
                    if 'code' in request.GET:
                        pro = Proyecto.objects.get(pk=request.GET.get('code'))
                        context['project'] = [{'project_id':pro.proyecto_id,'name':pro.nompro}]
                    if 'name' in request.GET:
                        context['project'] = [{'project_id':x.proyecto_id,'name':x.nompro} for x in Proyecto.objects.filter(nompro__icontains=request.GET.get('name')).order_by('nompro')]
                if 'subproject' in request.GET:
                    context['subproject'] = [{'subproject_id':x.subproyecto_id, 'name':x.nomsub, 'project_id':x.proyecto_id} for x in Subproyecto.objects.filter(proyecto_id=request.GET.get('pro')).order_by('nomsub')]
                if 'sector' in request.GET:
                    context['sector'] = [{'sector_id':x.sector_id, 'name':x.nomsec, 'plane':x.planoid, 'project_id':x.proyecto_id, 'subproject_id':x.subproyecto_id} for x in Sectore.objects.filter(proyecto_id=request.GET.get('pro'), subproyecto_id=request.GET.get('sub') if request.GET.get('sub') != '' else None)]
                if 'materials' in request.GET:
                    context['materials'] = [
                        {
                            'id': x.id,
                            'materials_id': x.materiales_id,
                            'name': x.materiales.matnom,
                            'measure': x.materiales.matmed,
                            'unit': x.materiales.unidad.uninom,
                            'brand': x.brand.brand,
                            'model': x.model.model,
                            'quantity': x.cantidad,
                            'price': x.precio
                        }
                        for x in MetProject.objects.filter(proyecto_id=request.GET['pro'], subproyecto_id=request.GET.get('sub') if request.GET.get('sub') != '' else None, sector_id=request.GET.get('sec')).order_by('materiales__matnom')
                    ]
                    if context['materials']:
                        context['materials'] = [
                            {
                                'id': x.id,
                                'materials_id': x.materiales_id,
                                'name': x.materiales.matnom,
                                'measure': x.materiales.matmed,
                                'unit': x.materiales.unidad.uninom,
                                'brand': x.brand.brand,
                                'model': x.model.model,
                                'quantity': x.cantidad,
                                'price': x.precio
                            }
                            for x in Metradoventa.objects.filter(proyecto_id=request.GET['pro'], subproyecto_id=request.GET.get('sub') if request.GET.get('sub') != '' else None, sector_id=request.GET.get('sec')).order_by('materiales__matnom')
                        ]
                context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if 'paste' in request.POST:
                    mats = request.POST.getlist('materials[]')
                    mven = Metradoventa.objects.filter(proyecto_id=request.POST.get('cpro'), subproyecto_id=request.POST.get('csub') if request.POST.get('csub') != '' else None, sector_id=request.POST.get('csec'), materiales_id__in=mats)
                    mmet = MetProject.objects.filter(proyecto_id=request.POST.get('cpro'), subproyecto_id=request.POST.get('csub') if request.POST.get('csub') != '' else None, sector_id=request.POST.get('csec'), materiales_id__in=mats)
                    copyList = None
                    if mmet.count() > mven.count():
                        copyList = mmet
                    else:
                        copyList = mven
                    for x in copyList:
                        obj = Metradoventa.objects.filter(proyecto_id=request.POST.get('pro'), subproyecto_id=request.POST.get('sub') if request.POST.get('sub') != '' else None, sector_id=request.POST.get('sec'), materiales_id=x.materiales_id)

                        if obj:
                            obj.cantidad = (x.cantidad + obj.cantidad)
                        else:
                            obj = Metradoventa()
                            obj.cantidad = x.cantidad

                        obj.proyecto_id = request.POST.get('pro')
                        obj.subproyecto_id = request.POST.get('sub')
                        obj.sector_id = request.POST.get('sec')
                        obj.materiales_id = x.materiales_id
                        obj.precio = x.precio
                        obj.brand_id = obj.brand_id
                        obj.model_id = x.model_id
                        obj.flag = True
                        obj.save()
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

class TreePath(View):
    def post(self, request, *args, **kwargs):
        path = uploadFiles.listDir(request.POST.get('dir'))
        return HttpResponse(path, 'text/plain')

# Request IVA by year
class GetIVAYear(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            if request.is_ajax():
                if 'percentigv' in request.GET:
                    if 'year' in request.GET:
                        try:
                            conf = Configuracion.objects.get(periodo__exact=request.GET.get('year'))
                            context['igv'] = conf.igv
                        except ObjectDoesNotExist, e:
                            context['igv'] = search.getigvCurrent()
                    else:
                        context['igv'] = search.getigvCurrent()
                    context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return self.render_to_json_response(context)

class GetNumberLiteral(JSONResponseMixin, View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            context['literal'] = globalVariable.convertNumberLiteral(float(request.GET.get('number')))
            context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return self.render_to_json_response(context)

# Search Group materials
class SearchGroupMaterials(JSONResponseMixin, View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if 'searchGroupMaterial' in request.GET:
                    gl = GroupMaterials.objects.filter(materials_id=request.GET.get('materials'))
                    if gl:
                        context['result'] = True
                        context['list'] = [
                            {
                                'mgroup': x.mgroup_id,
                                'description': x.description,
                                'materials': x.materials_id,
                                'name': '%s - %s'%(x.materials.matnom,x.materials.matmed),
                                'type': x.tgroup_id,
                                'tdesc': x.tgroup.typeg
                            }
                            for x in gl
                        ]
                        context['result'] = True
                    else:
                        pt = request.GET.get('materials')[0:12]
                        gl = GroupMaterials.objects.filter(parent=pt)
                        if gl:
                            context['list'] = [
                                {
                                    'mgroup': x.mgroup_id,
                                    'description': x.description,
                                    'materials': x.materials_id,
                                    'name': '%s - %s'%(x.materials.matnom,x.materials.matmed),
                                    'type': x.tgroup_id,
                                    'tdesc': x.tgroup.typeg
                                }
                                for x in gl
                            ]
                            context['result'] = True
                            context['parent'] = True
                        else:
                            context['result'] = False
                    context['status'] = True
                if 'DetailsGroupMaterials' in request.GET:
                    context['details'] = [
                        {
                            'materials': x.materials_id,
                            'name': x.materials.matnom,
                            'diameter': x.materials.matmed,
                            'unit': x.materials.unidad.uninom,
                            'quantity': x.quantity
                        }
                        for x in DetailsGroup.objects.filter(mgroup_id=request.GET.get('mgroup')).order_by('materials__matnom')
                    ]
                    for x in DetailsGroup.objects.filter(mgroup_id=request.GET.get('mgroup')).order_by('materials__matnom'):
                        context[x.materials_id] = [
                            {
                                'materials': m.materiales_id,
                                'meter': m.matmed
                            }
                            for m in Materiale.objects.filter(materiales_id__startswith=x.materials_id[0:12])
                        ]
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

# class GetAllAccounts(JSONResponseMixin, View):

#     @method_decorator(login_required)
#     def post(self, request, *args, **kwargs):
#         context = dict()
#         if request.is_ajax():
#             try:

#             except ObjectDoesNotExist, e:
#                 context['raise'] = e.__str__()
#                 context['status'] = False
#             return self.render_to_json_response(context)

class SystemEmails(JSONResponseMixin, View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            if 'allmails' in request.POST:
                context['for'] = globalVariable.emails #[ x.email for x in User.objects.all()]
                context['status'] = True
            if 'saveEmail' in request.POST:
                obj = Emails()
                obj.email = request.user.email
                obj.empdni_id = request.user.get_profile().empdni_id
                obj.fors = request.POST.get('forsb')
                if 'ccb' in request.POST:
                    obj.cc = request.POST.get('ccb')
                if 'ccob' in request.POST:
                    obj.cco = request.POST.get('ccob')
                obj.issue = request.POST.get('issue')
                obj.body = request.POST.get('body')
                if 'pwdmailer' in request.POST:
                    obj.account = True
                else:
                    obj.account = False
                obj.save()
                context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return self.render_to_json_response(context)

class KeyConfirmMan(JSONResponseMixin, View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            if 'genKeyConf' in request.POST:
                try:
                    if 'verify' in request.POST:
                        key = genkeys.GeneratekeysConfirm()
                        obj = KeyConfirm.objects.get(empdni_id=request.user.get_profile().empdni_id, code=request.POST.get('code') if request.POST.get('code') != '' else None)
                        obj.key = key
                        obj.save()
                        context['key'] = key
                    else:
                        obj = KeyConfirm()
                        key = genkeys.GeneratekeysConfirm()
                        obj.empdni_id = request.user.get_profile().empdni_id
                        obj.email = request.POST.get('email')
                        obj.code = request.POST.get('code') if request.POST.get('code') != '' else ''
                        obj.desc = request.POST.get('desc') if request.POST.get('desc') != '' else ''
                        obj.key = key
                        obj.save()
                        context['key'] = key
                except ObjectDoesNotExist:
                    obj = KeyConfirm()
                    key = genkeys.GeneratekeysConfirm()
                    obj.empdni_id = request.user.get_profile().empdni_id
                    obj.email = request.POST.get('email')
                    obj.code = request.POST.get('code') if request.POST.get('code') != '' else ''
                    obj.desc = request.POST.get('desc') if request.POST.get('desc') != '' else ''
                    obj.key = key
                    obj.save()
                    context['key'] = key
                context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return self.render_to_json_response(context)

class ProjectYear(JSONResponseMixin, View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            year = Proyecto.objects.get(pk=request.GET.get('pro')).registrado.strftime('%Y')
            context['year'] = year
            context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = str(e)
            context['status'] = False
        return self.render_to_json_response(context)

#############################################################################
##                                   Export Data
#############################################################################
class ExportMetProject(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            head = Sectore.objects.get(proyecto_id=kwargs['pro'], subproyecto_id=None, sector_id=kwargs['sec'])
            queryset = MetProject.objects.filter(proyecto_id=kwargs['pro'], subproyecto_id=None, sector_id=kwargs['sec']).order_by('materiales__matnom')
            if queryset:
                response = HttpResponse(content_type='text/csv')
                disposition = ''
                response['Content-Disposition'] = 'attachment; filename="%s.csv"'%(head.nomsec)
                writer = csv.writer(response)
                writer.writerow(['Código','Descripción','Diametro','Unidad','Marca','Modelo','Cantidad'])
                [writer.writerow([
                    x.materiales_id,
                    x.materiales.matnom.encode('utf-8'),
                    x.materiales.matmed.encode('utf-8'),
                    x.materiales.unidad.uninom,
                    x.brand.brand,
                    x.model.model,
                    x.cantidad]) for x in queryset]
                return response
        except ObjectDoesNotExist, e:
            raise Http404(e)


class ExportMaterialsDB(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # context = dict()
        try:
            queryset = Materiale.objects.order_by('matnom')
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="materials.csv"'
            writer = csv.writer(response)
            writer.writerow(['Código', 'Descripción', 'Diametro', 'Unidad'])
            if queryset:
                [
                    writer.writerow(
                        [
                            x.materiales_id.encode('utf-8'),
                            x.matnom.encode('utf-8'),
                            x.matmed.encode('utf-8'),
                            x.unidad.uninom.encode('utf-8')
                        ]
                    )
                    for x in queryset
                ]
            else:
                writer.writerow(['Any materials found'])
            return response
        except ObjectDoesNotExist, e:
            raise Http404(e)


class EmailsForsProject(JSONResponseMixin, View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'getfors' in request.GET:
                    fors = Emails.objects.filter(
                        issue__contains=request.GET['name']).order_by('-id')[0]
                    context['fors'] = fors.fors
                    context['status'] = True
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
