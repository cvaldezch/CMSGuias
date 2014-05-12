#-*- Encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, TemplateDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from CMSGuias.apps.almacen import models
from CMSGuias.apps.almacen import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from django.utils import simplejson
import datetime

##
#  Declare variables
##
FORMAT_DATE_STR = "%Y-%m-%d"

@login_required(login_url='/SignUp/')
def view_pedido(request):
	try:
		if request.method == 'GET':
			return render_to_response('almacen/pedido.html',context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')

@login_required(login_url='/SignUp/')
def view_keep_customers(request):
	try:
		if request.method == 'GET':
			lista = models.Cliente.objects.values('ruccliente_id','razonsocial','direccion','telefono').filter(flag=True).order_by('razonsocial')			
			ctx = { "lista": lista }
			return render_to_response("almacen/customers.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "ruc" in request.POST:
				data = {}
				try:
					obj = models.Cliente.objects.get(pk=request.POST.get('ruc'))
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
			if models.Cliente.objects.filter(pk=request.POST.get('ruccliente_id')).count() > 0:
				add = models.Cliente.objects.get(pk=request.POST.get('ruccliente_id'))
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
		c = models.Cliente.objects.get(pk__exact=ruc)
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
			lista = models.Proyecto.objects.filter(flag=True).order_by("nompro")
			return render_to_response('almacen/project.html',{"lista":lista, "tsid": u""},context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "proid" in request.POST:
				data = {}
				try:
					# sectores
					obj = models.Sectore.objects.filter(proyecto_id=request.POST.get('proid'))
					obj.status = 'DA'
					obj.flag = False
					obj.save()
					obj = models.Subproyecto.objects.filter(proyecto_id=request.POST.get('proid'))
					obj.status = 'DA'
					obj.flag = False
					obj.save()
					obj = models.Proyecto.objects.get(pk=request.POST.get('proid'))
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
			if models.Proyecto.objects.filter(pk=request.POST.get('proyecto_id')).count() > 0:
				add = models.Proyecto.objects.get(pk=request.POST.get('proyecto_id'))
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
						cod = models.Proyecto.objects.all().aggregate(Max('proyecto_id'))
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
		c = models.Proyecto.objects.get(pk__exact=proid)
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
			lista = models.Sectore.objects.filter(flag=True,proyecto__flag=True,proyecto_id__exact=pid,subproyecto_id=None if sid.strip() == "" else sid).order_by("sector_id")
			return render_to_response('almacen/sectores.html',{"lista":lista,"pid":pid,"sid":sid}, context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "sec" in request.POST:
				data = {}
				try:
					obj = models.Sectore.objects.get(proyecto_id=pid,subproyecto_id=None if sid.strip() == "" else sid,sector_id=request.POST.get('sec'))
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
		sec = models.Sectore.objects.get(proyecto_id=pid,subproyecto_id=None if sid == "" else sid, sector_id=cid)
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
			lista = models.Subproyecto.objects.filter(flag=True,proyecto__flag=True,proyecto_id__exact=pid).order_by("subproyecto_id")
			return render_to_response('almacen/subproject.html',{"lista":lista,"pid":pid,"sid":""},context_instance=RequestContext(request))
		elif request.method == 'POST':
			if "sid" in request.POST:
				data = {}
				try:
					obj = models.Sectore.objects.filter(proyecto_id=pid,subproyecto_id=request.POST.get('sid'))
					obj.delete()
					obj = models.Subproyecto.objects.get(subproyecto_id=request.POST.get('sid'),proyecto_id=pid)
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
		sub = models.Subproyecto.objects.get(flag=True,proyecto__flag=True,proyecto_id__exact=pid,subproyecto_id=sid)
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
			lista = models.Almacene.objects.filter(flag=True).order_by('nombre')
			ctx = { "lista": lista }
			return render_to_response("upkeep/almacenes.html",ctx,context_instance=RequestContext(request))
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
				c_old = models.Almacene.objects.all().aggregate(Max('almacen_id'))
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
		al = models.Almacene.objects.get(pk=aid)
		if request.method == 'GET':
			form = forms.addAlmacenesForm(instance=al)
			ctx = { "form": form }
			return render_to_response("upkeep/editalmacen.html",ctx,context_instance=RequestContext(request))
		elif request.method == 'POST':
			pass
	except TemplateDoesNotExist, e:
		messages("Template not found")
		raise Http404