#-*- Encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.contrib import messages
#from attendance.apps.almacen import models
from CMSGuias.apps.home.forms import signupForm, logininForm
from django.db.models import Count
# necesario para el login y autenticacion
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

@login_required(login_url='/SignUp/')
def view_home(request):
	if request.method == 'GET':
		return render_to_response('home/home.html',{},context_instance=RequestContext(request))

def login_view(request):
	try:
		message = ""
		if request.user.is_authenticated():
			return HttpResponseRedirect('/')
		else:
			if request.method == 'POST':
				#if request.POST['username'] == None || request.POST['password'] == None:
				#	return render_to_response('home/login.html',{m},context_instance=RequestContext(request))
				form = logininForm(request.POST)
				if form.is_valid():
					username = form.cleaned_data['username']
					password = form.cleaned_data['password']
					usuario = authenticate(username=username,password=password)
					if usuario is not None and usuario.is_active:
						login(request,usuario)
						return HttpResponseRedirect('/')
					else:
						message = "Usuario o Password incorrecto"
				else:
					message = "Usuario o Password no son validos!"
			form = logininForm()
			ctx = { 'form': form, 'msg': message }
			return render_to_response('home/login.html',ctx,context_instance=RequestContext(request))
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')

def logout_view(request):
	try:
		logout(request)
		return HttpResponseRedirect('/')
	except TemplateDoesNotExist, e:
		messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
		raise Http404('Method no proccess')