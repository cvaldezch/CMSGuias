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
from CMSGuias.apps.tools import genkeys
from .models import *
from .forms import *


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

class LogoutView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            logout(request)
            return HttpResponseRedirect(reverse_lazy('vista_login'))
        except TemplateDoesNotExist, e:
            messages.error(request, 'No se a encontrado esta pagina!')
            raise Http404('Template Does Not Exist')

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

# CRUD Country
class CountryList(ListView):
    template_name = 'home/crud/country.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.GET.get('menu'):
            context['menu'] = request.GET.get('menu')
        context['country'] = Pais.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance= RequestContext(request))

class CountryCreate(CreateView):
    form_class = CountryForm
    model = Pais
    success_url = reverse_lazy('country_list')
    template_name = 'home/crud/country_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CountryCreate, self).dispatch(request, *args, **kwargs)

class CountryUpdate(UpdateView):
    form_class = CountryForm
    model = Pais
    slug_field = 'pais_id'
    slug_url_kwarg = 'pais_id'
    success_url = reverse_lazy('country_list')
    template_name = 'home/crud/country_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CountryUpdate, self).dispatch(request, *args, **kwargs)

class CountryDelete(DeleteView):
    model = Pais
    slug_field = 'pais_id'
    slug_url_kwarg = 'pais_id'
    success_url = reverse_lazy('country_list')
    template_name = 'home/crud/country_del.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CountryDelete, self).dispatch(request, *args, **kwargs)

# CRUD Departament
class DepartamentList(ListView):
    template_name = "home/crud/departament.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.GET.get('menu'):
            context['country'] = request.GET.get('menu')
        context['departament'] = Departamento.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

class DepartamentCreate(CreateView):
    form_class = DepartamentForm
    model = Departamento
    success_url = reverse_lazy('departament_list')
    template_name = 'home/crud/departament_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DepartamentCreate, self).dispatch(request, *args, **kwargs)

class DepartamentUpdate(UpdateView):
    form_class = DepartamentForm
    model = Departamento
    slug_field = 'departamento_id'
    slug_url_kwarg = 'departamento_id'
    success_url = reverse_lazy('departament_list')
    template_name = 'home/crud/departament_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DepartamentUpdate, self).dispatch(request, *args, **kwargs)

class DepartamentDelete(DeleteView):
    model = Departamento
    slug_field = 'departamento_id'
    slug_url_kwarg = 'departamento_id'
    success_url = reverse_lazy('departament_list')
    template_name = 'home/crud/departament_del.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DepartamentDelete, self).dispatch(request, *args, **kwargs)

# CRUD Province
class ProvinceList(ListView):
    template_name = "home/crud/province.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.GET.get('menu'):
            context['country'] = request.GET.get('menu')
        context['province'] = Provincia.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

class ProvinceCreate(CreateView):
    form_class = ProvinceForm
    model = Provincia
    success_url = reverse_lazy('province_list')
    template_name = 'home/crud/province_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProvinceCreate, self).dispatch(request, *args, **kwargs)

class ProvinceUpdate(UpdateView):
    form_class = ProvinceForm
    model = Provincia
    slug_field = 'provincia_id'
    slug_url_kwarg = 'provincia_id'
    success_url = reverse_lazy('province_list')
    template_name = 'home/crud/province_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProvinceUpdate, self).dispatch(request, *args, **kwargs)

class ProvinceDelete(DeleteView):
    model = Provincia
    slug_field = 'provincia_id'
    slug_url_kwarg = 'provincia_id'
    success_url = reverse_lazy('province_list')
    template_name = 'home/crud/province_del.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProvinceDelete, self).dispatch(request, *args, **kwargs)

# CRUD District
class DistrictList(ListView):
    template_name = "home/crud/district.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.GET.get('menu'):
            context['menu'] = request.GET.get('get')
        context['district'] = Distrito.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

class DistrictCreate(CreateView):
    form_class = DistrictForm
    model = Distrito
    success_url = reverse_lazy('district_list')
    template_name = 'home/crud/district_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DistrictCreate, self).dispatch(request, *args, **kwargs)

class DistrictUpdate(UpdateView):
    form_class = DistrictForm
    model = Distrito
    slug_field = 'distrito_id'
    slug_url_kwarg = 'distrito_id'
    success_url = reverse_lazy('district_list')
    template_name = 'home/crud/district_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DistrictUpdate, self).dispatch(request, *args, **kwargs)

class DistrictDelete(DeleteView):
    model = Distrito
    slug_field = 'distrito_id'
    slug_url_kwarg = 'distrito_id'
    success_url = reverse_lazy('district_list')
    template_name = 'home/crud/district_del.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DistrictDelete, self).dispatch(request, *args, **kwargs)

# CRUD Brand
class BrandList(ListView):
    template_name = 'home/crud/brand.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.GET.get('menu'):
            context['menu'] = request.GET.get('get')
        context['brand'] = Brand.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

class BrandCreate(CreateView):
    form_class = BrandForm
    model = Brand
    success_url = reverse_lazy('brand_list')
    template_name = 'home/crud/brand_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BrandCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.brand_id = genkeys.GenerateIdBrand()
        self.save()
        return super(BrandCreate, self).form_valid(form)

class BrandUpdate(UpdateView):
    form_class = BrandForm
    model = Brand
    slug_field = 'brand_id'
    slug_url_kwarg = 'brand_id'
    success_url = reverse_lazy('brand_list')
    template_name = 'home/crud/brand_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BrandUpdate, self).dispatch(request, *args, **kwargs)

class BrandDelete(DeleteView):
    model = Brand
    slug_field = 'brand_id'
    slug_url_kwarg = 'brand_id'
    success_url = reverse_lazy('brand_list')
    template_name = 'home/crud/brand_del.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BrandDelete, self).dispatch(request, *args, **kwargs)

# CRUD Model
class ModelList(ListView):
    template_name = 'home/crud/model.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.GET.get('menu'):
            context['menu'] = request.GET.get('get')
        context['model'] = Model.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

class ModelCreate(CreateView):
    form_class = ModelForm
    model = Model
    success_url = reverse_lazy('model_list')
    template_name = 'home/crud/model_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ModelCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.model_id = genkeys.GenerateIdModel()
        self.save()
        return super(BrandCreate, self).form_valid(form)

class ModelUpdate(UpdateView):
    form_class = ModelForm
    model = Model
    slug_field = 'model_id'
    slug_url_kwarg = 'model_id'
    success_url = reverse_lazy('model_list')
    template_name = 'home/crud/model_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ModelUpdate, self).dispatch(request, *args, **kwargs)

class ModelDelete(DeleteView):
    model = Model
    slug_field = 'model_id'
    slug_url_kwarg = 'model_id'
    success_url = reverse_lazy('model_list')
    template_name = 'home/crud/model_del.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ModelDelete, self).dispatch(request, *args, **kwargs)
