#-*- Encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext, TemplateDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from CMSGuias.apps.almacen import models
from CMSGuias.apps.home.models import Cliente, Almacene, Transportista, Conductore, Transporte, userProfile
from CMSGuias.apps.ventas.models import Proyecto, Sectore, Subproyecto
from CMSGuias.apps.almacen import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from django.utils import simplejson
from CMSGuias.apps.tools import genkeys
import datetime

##
#  Declare variables
##
FORMAT_DATE_STR = "%Y-%m-%d"

@login_required(login_url='/SignUp/')
def view_pedido(request):
	try:
		if request.method == 'GET':
			#print request.user.get_profile().empdni
			return render_to_response('almacen/pedido.html',context_instance=RequestContext(request))
		if request.method == 'POST':
			data = {}
			form = forms.addOrdersForm(request.POST,request.FILES)
			if form.is_valid():
				# bedside Orders
				add = form.save(commit=False)
				id = genkeys.GenerateIdOrders()
				add.pedido_id = id
				add.status= 'PE'
				add.flag = True
				add.save()
				# detail Orders Details
				tmpd = models.tmppedido.objects.filter(empdni__exact=request.user.get_profile().empdni)
				for x in tmpd:
					det = models.Detpedido()
					det.pedido_id = id
					det.materiales_id = x.materiales_id
					det.cantidad = x.cantidad
					det.cantshop = x.cantidad
					det.save()
				# saved niples of tmpniple
				tmpn = models.tmpniple.objects.filter(empdni__exact=request.user.get_profile().empdni)
				for x in tmpn:
					nip = models.Niple()
					nip.pedido_id = id
					nip.proyecto_id = request.POST.get('proyecto')
					nip.subproyecto_id = request.POST.get('subproyecto')
					nip.sector_id = request.POST.get('sector')
					nip.empdni = request.user.get_profile().empdni
					nip.materiales_id= x.materiales_id
					nip.cantidad = x.cantidad
					nip.cantshop = x.cantidad
					nip.metrado = x.metrado
					nip.tipo = x.tipo
					nip.save()
				# deleting tmps
				tmp = models.tmppedido.objects.filter(empdni__exact=request.user.get_profile().empdni)
				tmp.delete()
				tmp = models.tmpniple.objects.filter(empdni__exact=request.user.get_profile().empdni)
				tmp.delete()
				data['status']= True
			else:
				data['status']= False
			return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')

@login_required(login_url='/SignUp/')
def view_keep_customers(request):
	try:
		if request.method == 'GET':
			lista = Cliente.objects.values('ruccliente_id','razonsocial','direccion','telefono').filter(flag=True).order_by('razonsocial')			
			ctx = { "lista": lista }
			return render_to_response("almacen/customers.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "ruc" in request.POST:
				data = {}
				try:
					obj = Cliente.objects.get(pk=request.POST.get('ruc'))
					obj.flag = False
					obj.save()
					data['status'] = True
				except ObjectDoesNotExist, e:
					data['status'] = False
				return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')

@login_required(login_url='/SignUp/')
def view_keep_add_customers(request):
	try:
		info = "Iniciando"
		if request.method == 'POST':
			if Cliente.objects.filter(pk=request.POST.get('ruccliente_id')).count() > 0:
				add = Cliente.objects.get(pk=request.POST.get('ruccliente_id'))
				add.razonsocial = request.POST.get('razonsocial')
				add.pais_id = request.POST.get('pais')
				add.departamento_id = request.POST.get('departamento')
				add.provincia_id = request.POST.get('provincia')
				add.distrito_id = request.POST.get('distrito')
				add.direccion = request.POST.get('direccion')
				add.telefono = request.POST.get('telefono')
				add.flag = True
				add.save()
			else:
				form = forms.addCustomersForm(request.POST)
				if form.is_valid():
						add = form.save(commit=False)
						add.flag = True
						add.save()
			#form.save_m2m() # esto es para guardar las relaciones ManyToMany
			return HttpResponseRedirect("/almacen/keep/customers/")
		if request.method == 'GET':
			form = forms.addCustomersForm()
		ctx = { "form": form, "info": info }
		return render_to_response("almacen/addcustomers.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')

@login_required(login_url='/SignUp/')
def view_keep_edit_customers(request,ruc):
	try:
		c = Cliente.objects.get(pk__exact=ruc)
		if request.method == 'GET':
			form = forms.addCustomersForm(instance=c)
		elif request.method == 'POST':
			form = forms.addCustomersForm(request.POST,instance=c)
			if form.is_valid():
				edit = form.save(commit=False)
				edit.flag = True
				edit.save()
				return HttpResponseRedirect("/almacen/keep/customers/")
		ctx = { "form": form }
		return render_to_response("almacen/editcustomers.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')

# Project keep views
@login_required(login_url='/SignUp/')
def view_keep_project(request):
	try:
		if request.method == 'GET':
			lista = Proyecto.objects.filter(flag=True).order_by("nompro")
			return render_to_response('almacen/project.html',{"lista":lista, "tsid": u""},context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "proid" in request.POST:
				data = {}
				try:
					# sectores
					obj = Sectore.objects.filter(proyecto_id=request.POST.get('proid'))
					obj.status = 'DA'
					obj.flag = False
					obj.save()
					obj = Subproyecto.objects.filter(proyecto_id=request.POST.get('proid'))
					obj.status = 'DA'
					obj.flag = False
					obj.save()
					obj = Proyecto.objects.get(pk=request.POST.get('proid'))
					obj.status = 'DA'
					obj.flag = False
					obj.save()
					data['status'] = True
				except ObjectDoesNotExist, e:
					data['status'] = False
				return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')
@login_required(login_url='/SignUp/')
def view_keep_add_project(request):
	try:
		if request.method == 'POST':
			if Proyecto.objects.filter(pk=request.POST.get('proyecto_id')).count() > 0:
				add = Proyecto.objects.get(pk=request.POST.get('proyecto_id'))
				add.ruccliente_id = request.POST.get('ruccliente')
				add.nompro = request.POST.get('nompro')
				add.comienzo = datetime.datetime.strptime( request.POST.get('comienzo'), FORMAT_DATE_STR ).date() if request.POST.get('comienzo') is not None else datetime.datetime.today().date()
				add.fin = datetime.datetime.strptime(request.POST.get('fin'), FORMAT_DATE_STR).date() if request.POST.get('fin') is not None else None
				add.pais_id = request.POST.get('pais')
				add.departamento_id = request.POST.get('departamento')
				add.provincia_id = request.POST.get('provincia')
				add.distrito_id = request.POST.get('distrito')
				add.direccion = request.POST.get('direccion')
				add.obser = request.POST.get('obser')
				add.status = request.POST.get('status')
				add.flag = True
				add.save()
			else:
				form = forms.addProjectForm(request.POST)
				if form.is_valid():
						add = form.save(commit=False)
						# for table project have generate id
						cod = Proyecto.objects.all().aggregate(Max('proyecto_id'))
						if cod['proyecto_id__max'] is not None:
							aa = cod["proyecto_id__max"][2:4]
							an = datetime.datetime.today().strftime("%y")
							cou = cod["proyecto_id__max"][4:7]
							if int(an) > int(aa):
								aa = an
								cou = 1
							else:
								cou = ( int(cou) + 1 )
						else:
							aa = datetime.datetime.today().strftime("%y")
							cou = 1
						cod = "%s%s%s"%("PR",str(aa),"{:0>3d}".format(cou))
						add.proyecto_id = cod.strip()
						add.flag = True
						add.save()
			return HttpResponseRedirect("/almacen/keep/project/")
		if request.method == 'GET':
			form = forms.addProjectForm()
		ctx = { "form": form}
		return render_to_response("almacen/addproject.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')
@login_required(login_url='/SignUp/')
def view_keep_edit_project(request,proid):
	try:
		c = Proyecto.objects.get(pk__exact=proid)
		if request.method == 'GET':
			form = forms.addProjectForm(instance=c)
		elif request.method == 'POST':
			# print request.POST.get('proyecto_id')
			form = forms.addProjectForm(request.POST,instance=c)
			if form.is_valid():
				edit = form.save(commit=False)
				edit.flag = True
				#edit.proyecto_id = request.POST.get('proyecto_id')
				edit.save()
				return HttpResponseRedirect("/almacen/keep/project/")
		ctx = { "form": form, "idpro": proid }
		return render_to_response("almacen/editproject.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')
# Sectors keep views
@login_required(login_url='/SignUp/')
def view_keep_sec_project(request,pid,sid):
	try:
		if request.method == 'GET':
			lista = Sectore.objects.filter(flag=True,proyecto__flag=True,proyecto_id__exact=pid,subproyecto_id=None if sid.strip() == "" else sid).order_by("sector_id")
			return render_to_response('almacen/sectores.html',{"lista":lista,"pid":pid,"sid":sid}, context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "sec" in request.POST:
				data = {}
				try:
					obj = Sectore.objects.get(proyecto_id=pid,subproyecto_id=None if sid.strip() == "" else sid,sector_id=request.POST.get('sec'))
					obj.delete()
					data['status'] = True
				except ObjectDoesNotExist, e:
					data['status'] = False
				return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')
@login_required(login_url='/SignUp/')
def view_keep_add_sector(request,proid,sid):
	try:
		if request.method == 'POST':
	 		form = forms.addSectoresForm(request.POST)
			if form.is_valid():
				add = form.save(commit=False)
				add.proyecto_id = request.POST.get('proyecto_id')
				add.subproyecto_id = request.POST.get('subproyecto_id')
				add.flag = True
				add.save()
				url = "/almacen/keep/sectores/%s/%s/"%(proid,sid)
				return HttpResponseRedirect(url)
			else:
				form = forms.addSectoresForm(request.POST)
				msg = "No se a podido realizar la transacción."
				ctx = { "form": form, "pid": proid, "sid": sid, "msg": msg }
				return render_to_response("almacen/addsector.html",ctx,context_instance=RequestContext(request))
		if request.method == 'GET':
			form = forms.addSectoresForm()
			ctx = { "form": form, "pid": proid, "sid": sid }
			return render_to_response("almacen/addsector.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')
@login_required(login_url='/SignUp')
def view_keep_edit_sector(request,pid,sid,cid):
	try:
		sec = Sectore.objects.get(proyecto_id=pid,subproyecto_id=None if sid == "" else sid, sector_id=cid)
		if request.method == "GET":
			form = forms.addSectoresForm(instance=sec)
			ctx = { "form": form, "pid": pid, "sid": sid, "cid": cid }
			return render_to_response("almacen/editsector.html",ctx,context_instance=RequestContext(request))
		elif request.method == "POST":
			form = forms.addSectoresForm(request.POST,instance=sec)
			if form.is_valid():
				edit = form.save(commit=False)
				edit.proyecto_id = request.POST.get('proyecto_id')
				edit.subproyecto_id = request.POST.get('subproyecto_id')
				edit.flag = True
				edit.save()
				url = "/almacen/keep/sectores/%s/%s/"%(pid,sid)
				return HttpResponseRedirect(url)
			else:
				form = forms.addSectoresForm(request.POST)
				msg = "No se a podido realizar la transacción."
				ctx = { "form": form, "pid": proid, "sid": sid, "msg": msg }
				return render_to_response("almacen/addsector.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, "No se puede mostrar la pagina.")
		raise Http404("Method not proccess")
# Subproyectos keep views
@login_required(login_url='/SignUp/')
def view_keep_sub_project(request,pid):
	try:
		if request.method == 'GET':
			lista = Subproyecto.objects.filter(flag=True,proyecto__flag=True,proyecto_id__exact=pid).order_by("subproyecto_id")
			return render_to_response('almacen/subproject.html',{"lista":lista,"pid":pid,"sid":""},context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "sid" in request.POST:
				data = {}
				try:
					obj = Sectore.objects.filter(proyecto_id=pid,subproyecto_id=request.POST.get('sid'))
					obj.delete()
					obj = Subproyecto.objects.get(subproyecto_id=request.POST.get('sid'),proyecto_id=pid)
					obj.delete()
					data['status'] = True
				except ObjectDoesNotExist, e:
					data['status'] = False
				return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')
@login_required(login_url='/SignUp/')
def view_keep_add_subproyeto(request,pid):
	try:
		if request.method == 'GET':
			form = forms.addSubprojectForm()
			ctx = {"form":form,"pid":pid}
			return render_to_response("almacen/addsubproyecto.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			form = forms.addSubprojectForm(request.POST)
			if form.is_valid():
				add = form.save(commit=False)
				add.proyecto_id = request.POST.get('proyecto_id')
				add.flag = True
				add.save()
				url = "/almacen/keep/subproyectos/%s/"%(pid)
				return HttpResponseRedirect(url)
			else:
				print 'Form no valid'
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')
@login_required(login_url='/SignUp')
def view_keep_edit_subproyecto(request,pid,sid):
	try:
		sub = Subproyecto.objects.get(flag=True,proyecto__flag=True,proyecto_id__exact=pid,subproyecto_id=sid)
		if request.method == "GET":
			form = forms.addSubprojectForm(instance=sub)
			ctx = { "form": form, "pid": pid }
			return render_to_response("almacen/editsubproyecto.html",ctx,context_instance=RequestContext(request))
		elif request.method == "POST":
			form = forms.addSubprojectForm(request.POST,instance=sub)
			if form.is_valid():
				edit = form.save(commit=False)
				edit.proyecto_id = request.POST.get('proyecto_id')
				edit.flag = True
				edit.save()
				url = "/almacen/keep/subproyectos/%s/"%(pid)
				return HttpResponseRedirect(url)
			else:
				form = forms.addSubprojectForm(request.POST)
				msg = "No se a podido realizar la transacción."
				ctx = { "form": form, "pid": pid,"msg": msg }
				return render_to_response("almacen/addsector.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, "No se puede mostrar la pagina.")
		raise Http404("Method not proccess")
# Almacenes
@login_required(login_url='/SignUp/')
def view_stores(request):
	try:
		if request.method == 'GET':
			lista = Almacene.objects.filter(flag=True).order_by('nombre')
			ctx = { "lista": lista }
			return render_to_response("upkeep/almacenes.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			data = {}
			try:
				obj = Almacene.objects.get(pk=request.POST.get('aid'))
				obj.delete()
				data['status'] = True
			except ObjectDoesNotExist, e:
				data['status'] = False
			return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
@login_required(login_url='/SignUp/')
def view_stores_add(request):
	try:
		if request.method == 'GET':
			form = forms.addAlmacenesForm()
			ctx = { "form": form }
			return render_to_response("upkeep/addalmacen.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			form = forms.addAlmacenesForm(request.POST)
			if form.is_valid():
				add = form.save(commit=False)
				# generate id for Stores
				c_old = Almacene.objects.all().aggregate(Max('almacen_id'))
				if c_old['almacen_id__max'] is not None:
					cont = c_old['almacen_id__max'][2:4]
					cont = int(cont) + 1
				else:
					cont = 1
				add.almacen_id = "AL%s"%("{:0>2d}".format(cont))
				add.flag = True
				add.save()
				return HttpResponseRedirect("/almacen/upkeep/stores/")
			else:
				form = forms.addAlmacenesForm(request.POST)
				ctx = { "form": form, "msg": "Transaction unrealized." }
				return render_to_response("upkeep/addalmacen.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
@login_required(login_url='/SignUp/')
def view_stores_edit(request,aid):
	try:
		al = Almacene.objects.get(pk=aid)
		if request.method == 'GET':
			form = forms.addAlmacenesForm(instance=al)
			ctx = { "form": form, "aid": aid }
			return render_to_response("upkeep/editalmacen.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			form = forms.addAlmacenesForm(request.POST, instance=al)
			if form.is_valid():
				edit = form.save(commit=False)
				edit.flag = True
				edit.save()
				url = "/almacen/upkeep/stores/"
				return HttpResponseRedirect(url)
			else:
				form = forms.addSubprojectForm(request.POST)
				msg = "No se a podido realizar la transacción."
				ctx = { "form": form, "almacen_id": almacen_id,"msg": msg }
				return render_to_response("almacen/addsector.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
# Transportistas
@login_required(login_url='/SignUp/')
def view_carrier(request):
	try:
		if request.method == 'GET':
			lista = Transportista.objects.filter(flag=True).order_by('tranom')
			ctx = { "lista": lista }
			return render_to_response("upkeep/transportista.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			data = {}
			if "ruc" in request.POST:
				try:
					# delete conductors
					obj = Conductore.objects.filter(traruc_id__exact=request.POST.get('ruc'))
					obj.delete()
					# delete Transport
					obj = Transporte.objects.filter(traruc_id__exact=request.POST.get('ruc'))
					obj.delete()
					# delete carrier
					obj = Transportista.objects.get(pk=request.POST.get('ruc'))
					obj.delete()
					data['status'] = True
				except ObjectDoesNotExist, e:
					data['status'] = False
				return HttpResponse(simplejson.dumps(data),mimetype='application/json')
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
@login_required(login_url="/SignUp/")
def view_carrier_add(request):
	try:
		if request.method == 'GET':
			form = forms.addCarrierForm()
			ctx = { "form": form }
			return render_to_response("upkeep/addcarrier.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			form = forms.addCarrierForm(request.POST)
			if form.is_valid():
				add = form.save(commit=False)
				add.flag = True
				add.save()
				return HttpResponseRedirect('/almacen/upkeep/carrier/')
			else:
				form = forms.addCarrierForm(request.POST)
				ctx = { "form": form }
				return render_to_response("upkeep/addcarrier.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
@login_required(login_url='/SignUp/')
def view_carrier_edit(request,ruc):
	try:
		t = Transportista.objects.get(pk=ruc)
		if request.method == 'GET':
			form = forms.addCarrierForm(instance=t)
			return render_to_response("upkeep/editcarrier.html",{"form":form,"ruc":ruc},context_instance=RequestContext(request))
		elif request.method == 'POST':
			form = forms.addCarrierForm(request.POST,instance=t)
			if form.is_valid():
				edit = form.save(commit=False)
				edit.flag =  True
				edit.save()
				return HttpResponseRedirect('/almacen/upkeep/carrier/')
			else:
				form = forms.addSubprojectForm(request.POST)
				msg = "No se a podido realizar la transacción."
				ctx = { "form": form, "almacen_id": almacen_id,"msg": msg }
				return render_to_response("almacen/addsector.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
# Transport
@login_required(login_url='/SignUp/')
def view_transport(request,ruc):
	try:
		if request.method == 'GET':
			lista = Transporte.objects.filter(flag=True,traruc_id=ruc)
			print lista
			ctx = { "lista": lista, "ruc":ruc, "nom": lista[0].traruc.tranom if len(lista) > 0 else "" }
			return render_to_response("upkeep/transport.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "nropla" in request.POST:
				data = {}
				try:
					obj = Transporte.objects.get(traruc_id=ruc,condni_id=request.POST.get('nropla'))
					obj.delete()
					data['status'] = True
				except ObjectDoesNotExist, e:
					data['status'] = False
				return HttpResponse(simplejson.dumps(data),mimetype='application/json')
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
@login_required(login_url='/SignUp/')
def view_transport_add(request,tid):
	try:
		if request.method == 'GET':
			form = forms.addTransportForm()
			ctx = { "form": form, "tid": tid }
			return render_to_response("upkeep/addtransport.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			form = forms.addTransportForm(request.POST)
			if form.is_valid():
				add = form.save(commit=False)
				add.traruc_id = request.POST.get('traruc_id')
				add.flag = True
				add.save()
				return HttpResponseRedirect('/almacen/upkeep/transport/%s'%tid)
			else:
				form = forms.addTransportForm(request.POST)
				ctx = { "form": form, "tid": tid }
				return render_to_response("upkeep/addtransport.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
@login_required(login_url="/SignUp/")
def view_transport_edit(request,cid,tid):
	try:
		t = Transporte.objects.get(traruc_id=cid,nropla_id=tid)
		if request.method == 'GET':
			form = forms.addTransportForm(instance=t)
			return render_to_response("upkeep/edittransport.html",{"form": form, "cid":cid, "tid": tid}, context_instance=RequestContext(request))
		if request.method == 'POST':
			form = forms.addTransportForm(request.POST, instance=t)
			if form.is_valid():
				edit = form.save(commit=True)
				return HttpResponseRedirect("/almacen/upkeep/transport/%s/"%cid)
			else:
				form = forms.addTransportForm(request.POST)
				return render_to_response("upkeep/edittransport.html",{"form": form, "cid":cid, "tid": tid}, context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
# Conductor
@login_required(login_url='/SignUp/')
def view_conductor(request,ruc):
	try:
		if request.method == 'GET':
			lista = Conductore.objects.filter(flag=True,traruc_id=ruc)
			print lista
			ctx = { "lista": lista, "ruc":ruc, "nom": lista[0].traruc.tranom if len(lista) > 0 else "" }
			return render_to_response("upkeep/conductor.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "condni" in request.POST:
				data = {}
				try:
					obj = Conductore.objects.get(traruc_id=ruc,condni_id=request.POST.get('condni'))
					obj.delete()
					data['status'] = True
				except ObjectDoesNotExist, e:
					data['status'] = False
				return HttpResponse(simplejson.dumps(data),mimetype='application/json')
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
@login_required(login_url='/SignUp/')
def view_conductor_add(request,tid):
	try:
		if request.method == 'GET':
			form = forms.addConductorForm()
			ctx = { "form": form, "tid": tid }
			return render_to_response("upkeep/addconductor.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			form = forms.addConductorForm(request.POST)
			if form.is_valid():
				add = form.save(commit=False)
				add.traruc_id = request.POST.get('traruc_id')
				add.flag = True
				add.save()
				return HttpResponseRedirect('/almacen/upkeep/conductor/%s'%tid)
			else:
				form = forms.addConductorForm(request.POST)
				ctx = { "form": form, "tid": tid }
				return render_to_response("upkeep/addconductor.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404
@login_required(login_url="/SignUp/")
def view_conductor_edit(request,cid,tid):
	try:
		t = Conductore.objects.get(traruc_id=cid,condni_id=tid)
		if request.method == 'GET':
			form = forms.addConductorForm(instance=t)
			return render_to_response("upkeep/editconductor.html",{"form": form, "cid":cid, "tid": tid}, context_instance=RequestContext(request))
		if request.method == 'POST':
			form = forms.addConductorForm(request.POST, instance=t)
			if form.is_valid():
				edit = form.save(commit=True)
				return HttpResponseRedirect("/almacen/upkeep/conductor/%s/"%cid)
			else:
				form = forms.addConductorForm(request.POST)
				return render_to_response("upkeep/editconductor.html",{"form": form, "cid":cid, "tid": tid}, context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404

"""
  request Orders
"""
# pending request Orders
@login_required(login_url='/SignUp/')
def view_orders_pending(request):
	try:
		if request.method == 'GET':
			lst= models.Pedido.objects.filter(flag=True,status='PE').order_by('-pedido_id')
			ctx= { 'lista': lst }
			return render_to_response('almacen/slopeorders.html',ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Error template not found")
		raise Http404("Process Error")
# list ortders attend request Orders
@login_required(login_url='/SignUp/')
def view_orders_list_approved(request):
	try:
		if request.method == 'GET':
			lst= models.Pedido.objects.filter(flag=True).exclude(Q(status='PE')|Q(status='AN')|Q(status='CO')).order_by('-pedido_id')
			ctx= { 'lista': lst }
			return render_to_response('almacen/listorderattend.html',ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages("Error template not found")
		raise Http404("Process Error")
# meet Orders
@login_required(login_url='/SignUp/')
def view_attend_order(request,oid):
	try:
		if request.method == 'GET':
			obj= get_object_or_404(models.Pedido,pk=oid,flag=True)
			det= get_list_or_404(models.Detpedido, pedido_id__exact=oid,flag=True)
			radio= ''
			for x in det:
				if x.cantshop <= 0:
					radio= 'disabled'
					break
			nipples= get_list_or_404(models.Niple.objects.order_by('metrado'),pedido_id__exact=oid,flag=True)
			usr= userProfile.objects.get(empdni__exact=obj.empdni)
			tipo= {"A":"Roscado","B":"Ranurado","C":"Rosca-Ranura"}
			ctx= { 'orders': obj, 'det': det, 'nipples': nipples, 'usr': usr,'tipo':tipo,'radio':radio }
			return render_to_response('almacen/attendorder.html',ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			try:
				import json
				data= {}
				# recover list of materials 
				mat= json.loads( request.POST.get('materials') )
				# recover list of nipples
				nip= json.loads( request.POST.get('nipples') )
				# variables
				cnm= 0
				cnn= 0
				ctn= 0
				# we walk the list materials and update items materials of details orders
				for c in range(len(mat)):
					cs= 0
					for x in range(len(nip)):
						if mat[c]['matid'] == nip[x]['matid']:
							cs+= (float(nip[x]['quantityshop']) * float(nip[x]['meter']) )
					ctn+= cs
					obj= models.Detpedido.objects.get(pedido_id__exact=request.POST.get('oid'),materiales_id__exact=mat[c]['matid'])
					# aqui hacer otro if 
					obj.cantshop=  (float(mat[c]['quantity']) - float(mat[c]['quantityshop'])) if (cs / 100 ) == float(mat[c]['quantity']) else (cs/100) if mat[c]['matid'][0:3] == "115" else (float(mat[c]['quantity']) - float(mat[c]['quantityshop']))
					#print (cs / 100 ) if mat[c]['matid'][0:3] == "115" else (float(mat[c]['quantity']) - float(mat[c]['quantityshop']))
					obj.cantguide= float(mat[c]['quantityshop'])
					obj.tag= "1"
					obj.save()
					cnm+= 1
				# we walk the list nipples and update tag of tables nipples
				for n in range(len(nip)):
					obj= models.Niple.objects.get(pk=nip[n]['nid'])
					obj.cantshop= int( float(nip[n]['quantity']) - float(nip[n]['quantityshop']) )
					obj.cantguide= int(float(nip[n]['quantityshop']))
					obj.tag= '1'
					obj.save()
					cnn+= 1
				# evaluation status orders
				# recover number of materials
				status= ''
				onm= models.Detpedido.objects.filter(pedido_id__exact=request.POST.get('oid'),cantshop__gt=0).exclude(tag='2').count()
				if onm > 0:
					status= 'IN'
				else:
					status= 'CO'
				# update status Bedside Orders
				obj = models.Pedido.objects.get(pk=request.POST.get('oid'))
				obj.status= status
				obj.save()
				data['sts']= status
				data['pass']= status
				data['status']= True
			except ObjectDoesNotExist, e:
				data['status']= False
			return HttpResponse(simplejson.dumps(data), mimetype="application/json" )
	except TemplateDoesNotExist, e:
		message("Error template not found")
		raise Http404
"""
	guide remision
"""
# generate guide remision of a orders
@login_required(login_url='/SignUp/')
def view_generate_guide_orders(request):
	try:
		if request.method == 'GET':
			#lst= get_list_or_404(models.Pedido.objects.exclude(Q(status='PE')|Q(status='AN')).order_by('-pedido_id'), flag=True )
			lst= models.Detpedido.objects.filter(tag='1').order_by('-pedido').distinct('pedido')
			ctx= { 'orders': lst }
			return render_to_response("almacen/generateGuide.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		message('Error Template not found')
		raise Http404
# request generate guide remision
@login_required(login_url='/SignUp/')
def view_generate_document_out(request,oid):
	try:
		if request.method == 'GET':
			orders= get_object_or_404(models.Pedido,flag=True,pedido_id__exact=oid)
			print orders
			trans= get_list_or_404(Transportista.objects.values('traruc_id','tranom'),flag=True)
			ctx= { 'oid': oid, 'trans': trans, 'orders': orders }
			return render_to_response("almacen/documentout.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			if request.is_ajax():
				form= forms.addGuideReferral(request.POST)
				if form.is_valid():
					data= {}
					try:
						add= form.save(commit=False)
						guidekeys= genkeys.GenerateSerieGuideRemision()
						add.guia_id= guidekeys
						add.status= 'GE'
						add.flag= True
						# commit true save bedside guide
						add.save()
						# save details guide referral
						# recover details orders
						det= models.Detpedido.objects.filter(pedido_id__exact=request.POST.get('pedido'),tag='1',flag=True)
						for x in det:
							obj= models.DetGuiaRemision()
							obj.guia_id= guidekeys
							obj.materiales_id= x.materiales_id
							obj.cantguide= x.cantguide
							obj.flag= True
							obj.save()
							ob = models.Detpedido.objects.get(pk__exact=x.id)
							ob.tag= '2' if x.cantshop <= 0 else '0'
							ob.save()
						# recover details nipples
						nip= models.Niple.objects.filter(pedido_id__exact=request.POST.get('pedido'),tag='1',flag=True)
						for x in nip:
							obj= models.NipleGuiaRemision()
							obj.guia_id= guidekeys
							obj.materiales_id= x.materiales_id
							obj.metrado= x.metrado
							obj.cantguide= x.cantguide
							obj.tipo= x.tipo
							obj.flag= True
							# save details niples for guide referral
							obj.save()
							ob= models.Niple.objects.get(pk__exact=x.id)
							ob.tag= '2' if x.cantshop <= 0 else '0'
							ob.save()
						data['status']= True
						data['guide']= guidekeys
					except ObjectDoesNotExist, e:
						data['status']= False
					return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	except TemplateDoesNotExist, e:
		message("Error: Template not found")
		raise Http404
# recover list guide referral for view and annular
@login_required(login_url='/SignUp/')
def view_list_guide_referral_success(request):
	try:
		if request.method == 'GET':
			if request.is_ajax():
				data= {}
				ls= []
				try:
					if request.GET.get('tra') == 'series':
						lst= models.GuiaRemision.objects.get(pk=request.GET.get('series'),status='GE',flag=True)
						ls= [{"item":1,"guia_id":lst.guia_id,"nompro":lst.pedido.proyecto.nompro,"traslado":lst.traslado.strftime(FORMAT_DATE_STR),"connom":lst.condni.connom}]
						data['status']= True
					elif request.GET.get('tra') == "dates":
						if request.GET.get('fecf') == '' and request.GET.get('feci') != '':
							star= datetime.datetime.strptime(request.GET.get('feci'), FORMAT_DATE_STR ).date()
							lst= models.GuiaRemision.objects.filter(traslado=star,status='GE',flag=True)
						elif request.GET.get('fecf') != '' and request.GET.get('feci') != '':
							star= datetime.datetime.strptime(request.GET.get('feci'), FORMAT_DATE_STR ).date()
							end= datetime.datetime.strptime(request.GET.get('fecf'), FORMAT_DATE_STR ).date()
							lst= models.GuiaRemision.objects.filter(traslado__range=[star,end],status='GE',flag=True)
						i= 1
						for x in lst:
							ls.append({"item":i,"guia_id":x.guia_id,"nompro":x.pedido.proyecto.nompro,"traslado":x.traslado.strftime(FORMAT_DATE_STR),"connom":x.condni.connom})
							i+= 1
						data['status']= True
				except ObjectDoesNotExist, e:
					data['status']= False
				data['list']= ls
				return HttpResponse(simplejson.dumps(data),mimetype="application/json")
			lst= models.GuiaRemision.objects.filter(status='GE',flag=True).order_by('-guia_id')[:10]
			ctx= {'guide':lst}
			return render_to_response("almacen/listguide.html",ctx,context_instance=RequestContext(request))
		if request.method == 'POST':
			data= {}
			try:
				obj= models.GuiaRemision.objects.get(pk=request.POST.get('series'),status='GE',flag=True)
				obj.status= 'AN'
				obj.flag= False
				obj.save()
				det= models.DetGuiaRemision.objects.filter(guia_id__exact=request.POST.get('series')).update(flag=False)
				nip= models.NipleGuiaRemision.objects.filter(guia_id__exact=request.POST.get('series')).update(flag=False)
				data['status']= True
			except ObjectDoesNotExist, e:
				data['status']= False
			return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	except TemplateDoesNotExist, e:
		raise Http404
# recover list guide referral for view and annular
@login_required(login_url='/SignUp/')
def view_list_guide_referral_canceled(request):
	try:
		if request.method == 'GET':
			if request.is_ajax():
				data= {}
				ls= []
				try:
					if request.GET.get('tra') == 'series':
						lst= models.GuiaRemision.objects.get(pk=request.GET.get('series'),status='AN',flag=False)
						ls= [{"item":1,"guia_id":lst.guia_id,"nompro":lst.pedido.proyecto.nompro,"traslado":lst.traslado.strftime(FORMAT_DATE_STR),"connom":lst.condni.connom}]
						data['status']= True
					elif request.GET.get('tra') == "dates":
						if request.GET.get('fecf') == '' and request.GET.get('feci') != '':
							star= datetime.datetime.strptime(request.GET.get('feci'), FORMAT_DATE_STR ).date()
							lst= models.GuiaRemision.objects.filter(traslado=star,status='AN',flag=False)
						elif request.GET.get('fecf') != '' and request.GET.get('feci') != '':
							star= datetime.datetime.strptime(request.GET.get('feci'), FORMAT_DATE_STR ).date()
							end= datetime.datetime.strptime(request.GET.get('fecf'), FORMAT_DATE_STR ).date()
							lst= models.GuiaRemision.objects.filter(traslado__range=[star,end],status='AN',flag=False)
						i= 1
						for x in lst:
							ls.append({"item":i,"guia_id":x.guia_id,"nompro":x.pedido.proyecto.nompro,"traslado":x.traslado.strftime(FORMAT_DATE_STR),"connom":x.condni.connom})
							i+= 1
						data['status']= True
				except ObjectDoesNotExist, e:
					data['status']= False
				data['list']= ls
				return HttpResponse(simplejson.dumps(data),mimetype="application/json")
			lst= models.GuiaRemision.objects.filter(status='AN',flag=False).order_by('-guia_id')[:10]
			ctx= {'guide':lst}
			return render_to_response("almacen/listguidecanceled.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		raise Http404