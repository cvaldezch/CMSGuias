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
from django.utils.simplejson import simplejson
import datetime

@login_required(login_url='/SignUp/')
def view_pedido(request):
	try:
		if request.method == 'GET':
			return render_to_response('almacen/pedido.html',context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')

@login_required(login_url='/SignUp/')
def view_keep_project(request):
	try:
		if request.method == 'GET':
			lista = models.Proyecto.objects.filter(flag=True).order_by("nompro")
			return render_to_response('almacen/project.html',{"lista":lista},context_instance=RequestContext(request))
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
def view_keep_add_project(request):
	try:
		if request.method == 'POST':
			if models.Proyecto.objects.filter(pk=request.POST.get('proyecto_id')).count() > 0:
				add = models.Proyecto.objects.get(pk=request.POST.get('proyecto_id'))
				# add.razonsocial = request.POST.get('razonsocial')
				# add.pais_id = request.POST.get('pais')
				# add.departamento_id = request.POST.get('departamento')
				# add.provincia_id = request.POST.get('provincia')
				# add.distrito_id = request.POST.get('distrito')
				# add.direccion = request.POST.get('direccion')
				# add.telefono = request.POST.get('telefono')
				# add.flag = True
				# add.save()
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
			form = forms.addProjectForm(request.POST,instance=c)
			if form.is_valid():
				edit = form.save(commit=False)
				edit.flag = True
				edit.save()
				return HttpResponseRedirect("/almacen/keep/project/")
		ctx = { "form": form }
		return render_to_response("almacen/editproject.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')