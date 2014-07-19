#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.contrib import messages
from django.db.models import Count
# necesario para el login y autenticacion
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from CMSGuias.apps.home.forms import signupForm, logininForm
from CMSGuias.apps.tools.redirectHome import RedirectModule
from .models import Cliente
from .forms import CustomersForm


class HomeManager(ListView):
    template_name = 'home/home.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        self.template_name = RedirectModule(request.user.get_profile().empdni.charge.area)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            form = logininForm()
        return render_to_response('home/login.html', {'form':form} ,context_instance=RequestContext(request))
        #return HttpResponseRedirect(reverse_lazy('vista_home'))

    def post(self, request, *args, **kwargs):
        message = ''
        form = logininForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(username=username,password=password)
            if usuario is not None and usuario.is_active:
                login(request, usuario)
                return HttpResponseRedirect(reverse_lazy('vista_home'))
            else:
                message = "Usuario o Password incorrecto"
        else:
            message = "Usuario o Password no son validos!"

        form = logininForm()
        ctx = { 'form': form, 'msg': message }
        return render_to_response('home/login.html', ctx, context_instance=RequestContext(request))

# def login_view(request):
#     try:
#         message = ""

#         else:
#             if request.method == 'POST':

#     except TemplateDoesNotExist, e:
#         messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
#         raise Http404('Method no proccess')

class LogoutView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            logout(request)
            return HttpResponseRedirect(reverse_lazy('vista_login'))
        except TemplateDoesNotExist, e:
            messages.error(request, 'No se a encontrado esta pagina!')
            raise Http404('Template Does Not Exist')

# def logout_view(request):
#     try:
#         logout(request)
#         return HttpResponseRedirect(reverse_lazy('vista_login'))
#     except TemplateDoesNotExist, e:
#         messages.error(request, 'Esta pagina solo acepta peticiones Encriptadas!')
#         raise Http404('Method no proccess')

# CRUD Customers
class CustomersList(ListView):
    template_name = 'home/crud/customers.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.GET.get('menu'):
            context['menu'] = request.GET.get('menu')
        context['object_list'] = Cliente.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

class CustomersCreate(CreateView):
    form_class = CustomersForm
    model = Cliente
    success_url = reverse_lazy('customers_list')
    template_name = 'home/crud/customers_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CustomersCreate, self).dispatch(request, *args, **kwargs)

class CustomersUpdate(UpdateView):
    form_class = CustomersForm
    model = Cliente
    success_url = reverse_lazy('customers_list')
    template_name = 'home/crud/customers_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CustomersUpdate, self).dispatch(request, *args, **kwargs)

class CustomersDelete(DeleteView):
    model = Cliente
    success_url = reverse_lazy('customers_list')
    template_name = 'home/crud/customers_del.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CustomersDelete, self).dispatch(request, *args, **kwargs)