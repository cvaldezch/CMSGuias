#-*- Encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from CMSGuias.apps.almacen import models
from CMSGuias.apps.almacen import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Count

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
			return render_to_response('almacen/project.html',context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')
	
@login_required(login_url='/SignUp/')
def view_keep_customers(request):
	try:
		if request.method == 'GET':
			lista = models.Cliente.objects.values('ruccliente_id','razonsocial','direccion','telefono').all().order_by('razonsocial')			
			ctx = { "lista": lista }
			return render_to_response("almacen/customers.html",ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')

@login_required(login_url='/SignUp/')
def view_keep_add_customers(request):
	try:
		info = "Iniciando"
		if request.method == 'POST':
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