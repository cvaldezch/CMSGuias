#-*- Encoding: utf-8 -*-
import json

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import simplejson
from django.core import serializers

from CMSGuias.apps.almacen import models
from CMSGuias.apps.home.models import Materiale, Almacene, Transporte, Conductore
from CMSGuias.apps.ventas.models import Proyecto, Sectore, Subproyecto


def get_description_materials(request):
    try:
        if request.method == 'GET':
            data = {'name':[]}
            name = Materiale.objects.values('matnom').filter(matnom__icontains=request.GET['nom']).distinct('matnom').order_by('matnom')
            i = 0
            for x in name:
                data['name'].append({'matnom':x['matnom'],'id':i})
                i+=1
            return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    except ObjectDoesNotExist:
        raise Http404

def get_meter_materials(request):
    try:
        if request.method == 'GET':
            data = { "list": [] }
            meter = Materiale.objects.values('matmed').filter(matnom__icontains=request.GET['matnom']).distinct('matmed').order_by('matmed')
            for x in meter:
                data["list"].append({ "matmed": x["matmed"] })
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    except ObjectDoesNotExist:
        raise Http404

def get_resumen_details_materiales(request):
    try:
        if request.method == 'GET':
            data = {'list': []}
            res = Materiale.objects.values('materiales_id','matnom','matmed','unidad').filter(matnom__icontains=request.GET['matnom'],matmed__icontains=request.GET['matmed'])[:1]
            data['list'].append({ "materialesid": res[0]['materiales_id'], "matnom": res[0]['matnom'], "matmed": res[0]['matmed'], "unidad": res[0]['unidad'] })
            return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    except ObjectDoesNotExist:
        raise e

class GetDetailsMaterialesByCode(DetailView):
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                mat = Materiale.objects.values('materiales_id','matnom','matmed','unidad').get(pk=request.GET.get('code'))
                context['list'] = {"materialesid": mat['materiales_id'], "matnom": mat['matnom'], "matmed": mat['matmed'], "unidad": mat['unidad']}
                context['status'] = True
            except ObjectDoesNotExist, e:
                raise e
                context['status'] = False
            return HttpResponse(simplejson.dumps(context), mimetype='application/json')

def save_order_temp_materials(request):
    try:
        data = {}
        if request.method == "POST":
            c = models.tmppedido.objects.filter(empdni__exact=request.POST['dni'],materiales_id__exact=request.POST['mid']).count()
            quantity_old = 0
            if c > 0:
                obj = models.tmppedido.objects.get(empdni__exact=request.POST['dni'],materiales_id__exact=request.POST['mid'])
                quantity_old = float(obj.cantidad)
            else:
                obj = models.tmppedido()
            obj.empdni = request.POST['dni']
            obj.materiales_id = request.POST['mid']
            obj.cantidad = ( float(request.POST['cant']) + quantity_old)
            obj.save()
            data['status'] = True
        else:
            data['status'] = False
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    except ObjectDoesNotExist, e:
        raise e

def update_order_temp_materials(request):
    try:
        data = {}
        if request.method == "POST":
            obj = models.tmppedido.objects.get(empdni__exact=request.POST['dni'],materiales_id__exact=request.POST['mid'])
            obj.cantidad = request.POST['cantidad']
            obj.save()
            data['status'] = True
        else:
            data['status'] = False
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    except ObjectDoesNotExist, e:
        raise e

def delete_order_temp_material(request):
    try:
        data = {}
        if request.method == "POST":
            obj = models.tmppedido.objects.get(empdni__exact=request.POST['dni'],materiales_id__exact=request.POST['mid'])
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
            obj = models.tmppedido.objects.filter(empdni__exact=request.POST['dni'])
            obj.delete()
            # here get object "Niples" tambien deberan ser eliminadas
            tmp = models.tmpniple.objects.filter(empdni__exact=request.POST.get('dni'))
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
            ls = models.tmppedido.objects.filter(empdni__exact=request.GET['dni']).order_by("materiales")
            #lista = [ {"cant": x.cantidad, "materiales_id": x.materiales_id, "matnom": x.materiales.matnom } for x in ls ]
            i = 1
            for x in ls:
                data['list'].append({"item": i, "materiales_id": x.materiales_id, "matnom": x.materiales.matnom, "matmed": x.materiales.matmed, "unidad": x.materiales.unidad_id, "cantidad": x.cantidad })
                i+=1
            data['status'] = True
        else:
            data['status'] = False
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
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
            ls = models.tmppedido.objects.filter(materiales__materiales_id__startswith='115').order_by("materiales")
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
            ls = models.tmpniple.objects.filter(empdni__exact=request.GET['dni'],materiales_id__exact=request.GET['mid']).order_by('metrado')
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
                obj = models.tmpniple()
            else:
                obj = models.tmpniple.objects.get(id=request.POST.get('id'))
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
            obj = models.tmpniple.objects.get(id__exact=request.POST.get('id'), materiales_id__exact=request.POST.get('mid'),empdni__exact=request.POST.get('dni'))
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
            obj = models.tmpniple.objects.filter(materiales_id__exact=request.POST.get('mid'))
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
                            obj, created= models.tmppedido.objects.get_or_create(materiales_id=mid,empdni=request.user.get_profile().empdni,defaults={'cantidad':cant.value})
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
                                obj, created= models.tmpniple.objects.get_or_create(materiales_id=mid,metrado=med,tipo=tipo,empdni=request.user.get_profile().empdni,defaults={'cantidad':cant})
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
            obj = models.Pedido.objects.get(pk=request.POST.get('oid'))
            obj.status = 'AP'
            obj.flag = True
            obj.save()
            data['status']= True
        except ObjectDoesNotExist, e:
            data['status']= False
            data['msg']= e
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
# cancel orders
def post_cancel_orders(request):
    if request.method == 'POST':
        data = {}
        try:
            obj = models.Pedido.objects.get(pk=request.POST.get('oid'))
            obj.status = 'AN'
            obj.flag = False
            obj.save()
            data['status']= True
        except ObjectDoesNotExist, e:
            data['status']= False
            data['msg']= e
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
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
class get_OrdersDetails(ListView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
          context = {}
          try:
              arr = json.loads(request.GET.get('orders'))
              queryset = models.Detpedido.objects.filter(pedido_id__in=arr).extra(select = { 'stock': "SELECT stock FROM almacen_inventario WHERE almacen_detpedido.materiales_id LIKE almacen_inventario.materiales_id AND periodo LIKE to_char(now(), 'YYYY')"},)
              queryset = queryset.values('materiales_id','materiales__matnom','materiales__matmed','materiales__unidad_id','stock','spptag')
              queryset = queryset.annotate(cantidad=Sum('cantshop'))
              context['list'] = [{'materiales_id': x['materiales_id'],'matnom': x['materiales__matnom'],'matmed':x['materiales__matmed'],'unidad':x['materiales__unidad_id'],'cantidad':x['cantidad'],'stock':x['stock'],'tag':x['spptag']} for x in queryset]
              context['status'] = True
          except ObjectDoesNotExist:
              context['sttatus'] = False
          return HttpResponse(simplejson.dumps(context),mimetype='application/json')

class SupplyDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        context = {}
        try:
            response = HttpResponse()
            response['content-type'] = 'application/json'
            response['mimetype'] = 'application/json'
            queryset = models.DetSuministro.objects.filter(suministro_id__exact=kwargs['sid'], flag=True)
            queryset = queryset.values('materiales_id','materiales__matnom','materiales__matmed','materiales__unidad_id')
            queryset = queryset.annotate(cantidad=Sum('cantshop')).order_by('materiales__matnom')
            context['status'] = True
            context['list'] = [{'materiales_id':x['materiales_id'],'materiales__matnom':x['materiales__matnom'],'materiales__matmed':x['materiales__matmed'],'materiales__unidad_id':x['materiales__unidad_id'],'cantidad':x['cantidad']} for x in queryset]
            response.write(simplejson.dumps(context))
        except Exception, e:
            context['status'] = False
        return response