#-*- Encoding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
#from django.views.generic import TemplateView
from django.contrib import messages
from CMSGuias.apps.almacen import models
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import simplejson

def get_description_materials(request):
	try:
		if request.method == 'GET':
			data = {'name':[]}
			name = models.Materiale.objects.values('matnom').filter(matnom__icontains=request.GET['nom']).distinct('matnom').order_by('matnom')
			i = 0
			#data['name'] = [ { 'matnom': x['matnom'], 'id': i+=1 } for x in name ]
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
			meter = models.Materiale.objects.values('matmed').filter(matnom__icontains=request.GET['matnom']).distinct('matmed').order_by('matmed')
			for x in meter:
				data["list"].append({ "matmed": x["matmed"] })
			return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	except ObjectDoesNotExist:
		raise Http404

def get_resumen_details_materiales(request):
	try:
		if request.method == 'GET':
			data = {'list': []}
			res = models.Materiale.objects.values('materiales_id','matnom','matmed','unidad').filter(matnom__icontains=request.GET['matnom'],matmed__icontains=request.GET['matmed'])[:1]
			data['list'].append({ "materialesid": res[0]['materiales_id'], "matnom": res[0]['matnom'], "matmed": res[0]['matmed'], "unidad": res[0]['unidad'] })
			return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	except ObjectDoesNotExist:
		raise e

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
			mat = models.Materiale.objects.values('materiales_id','matnom','matmed','unidad_id').get(pk=request.GET.get('mid'))
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