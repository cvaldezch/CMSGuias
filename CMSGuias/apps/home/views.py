# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.contrib import messages
from django.db.models import Count
# necesario para el login y autenticacion
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View

from CMSGuias.apps.home.forms import signupForm, logininForm
from CMSGuias.apps.tools.redirectHome import RedirectModule


class HomeManager(ListView):
    template_name = 'home/home.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        self.template_name = RedirectModule(request.user.get_profile().cargo.area)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

def login_view(request):
    try:
        message = ""
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            if request.method == 'POST':
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