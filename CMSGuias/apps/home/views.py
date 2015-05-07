#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import json

from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
# necesario para el login y autenticacion
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse_lazy
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from CMSGuias.apps.home.forms import signupForm, logininForm
from CMSGuias.apps.tools.redirectHome import RedirectModule
from CMSGuias.apps.tools import genkeys
from CMSGuias.apps.logistica.models import Compra, DetCompra
from .models import *
from .forms import *


class JSONResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            mimetype='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        return simplejson.dumps(context, encoding='utf-8')

class HomeManager(ListView):
    template_name = 'home/home.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            context = dict()
            com = Company.objects.get(pk='20428776110')
            request.session['company'] = {
                'ruc': com.ruc,
                'name': com.companyname,
                'address': com.address,
                'phone': com.phone
            }
            self.template_name = RedirectModule(request.user.get_profile().empdni.charge.area)
            return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        except TemplateDoesNotExist, e:
            raise e

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
            del request.session
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
        try:
            brand = Brand.objects.get(brand__icontains=self.object.brand)
            if brand:
                return HttpResponseRedirect(self.success_url)
        except ObjectDoesNotExist, e:
            self.object.brand_id = genkeys.GenerateIdBrand()
            self.object.save()
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
        try:
            model = Model.objects.get(model__icontains=self.object.model)
            if model:
                return HttpResponseRedirect(self.success_url)
        except Exception, e:
            self.object.model_id = genkeys.GenerateIdModel()
            self.object.save()
            return super(ModelCreate, self).form_valid(form)

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

class TGroupList(ListView):
    template_name = 'home/crud/tgroup.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.GET.get('menu'):
            context['menu'] = request.GET.get('get')
        context['tgroup'] = TypeGroup.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

class TGroupCreate(CreateView):
    form_class = TGroupForm
    model = TypeGroup
    success_url = reverse_lazy('tgroup_list')
    template_name = 'home/crud/tgroup_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TGroupCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            tgroup = TypeGroup.objects.get(typeg__icontains=self.object.typeg)
            if tgroup:
                return HttpResponseRedirect(self.success_url)
        except Exception, e:
            self.object.tgroup_id = genkeys.GenerateIdTypeGroupMaterials()
            self.object.save()
            return super(TGroupCreate, self).form_valid(form)

class TGroupUpdate(UpdateView):
    form_class = TGroupForm
    model = TypeGroup
    slug_field = 'tgroup_id'
    slug_url_kwarg = 'tgroup_id'
    success_url = reverse_lazy('tgroup_list')
    template_name = 'home/crud/tgroup_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TGroupUpdate, self).dispatch(request, *args, **kwargs)

class TGroupDelete(DeleteView):
    model = TypeGroup
    slug_field = 'tgroup_id'
    slug_url_kwarg = 'tgroup_id'
    success_url = reverse_lazy('tgroup_list')
    template_name = 'home/crud/tgroup_del.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TGroupDelete, self).dispatch(request, *args, **kwargs)

class GMaterialsList(ListView):
    template_name = 'home/crud/gmaterials.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.GET.get('menu'):
            context['menu'] = request.GET.get('get')
        context['gmaterials'] = GroupMaterials.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

class GMaterialsCreate(CreateView):
    form_class = GMaterialsForm
    model = GroupMaterials
    success_url = reverse_lazy('gmaterials_list')
    template_name = 'home/crud/gmaterials_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GMaterialsCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            tgroup = GroupMaterials.objects.get(materials_id=self.object.materials, tgroup_id=self.object.tgroup)
            #print tgroup, 'tgroup question'
            if tgroup:
                return HttpResponseRedirect(self.success_url)
            else:
                self.object.mgroup_id = genkeys.GenerateIdGroupMaterials()
                self.object.save()
                return super(GMaterialsCreate, self).form_valid(form)
        except Exception, e:
            self.object.mgroup_id = genkeys.GenerateIdGroupMaterials()
            self.object.save()
            return super(GMaterialsCreate, self).form_valid(form)

class GMaterialsUpdateSave(UpdateView):
    form_class = GMaterialsForm
    model = GroupMaterials
    slug_field = 'mgroup_id'
    slug_url_kwarg = 'mgroup_id'
    success_url = reverse_lazy('gmaterials_list')
    template_name = 'home/crud/gmaterials_form.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(pk=request.POST.get('mgroup_id'))
        form = self.form_class(request.POST, instance=obj)
        print form.is_valid()
        if form.is_valid():
            form.save()
        else:
            return HttpResponseRedirect('/gmaterials/edit/%s/'%request.POST.get('mgroup_id'))
        return HttpResponseRedirect(self.success_url)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(GMaterialsUpdateSave, self).dispatch(request, *args, **kwargs)

class GMaterialsUpdate(TemplateView):
    #model = GroupMaterials
    # slug_field = 'mgroup_id'
    # slug_url_kwarg = 'mgroup_id'
    template_name = 'home/crud/gmaterials_form.html'

    #@method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        context['value'] = get_object_or_404(GroupMaterials, pk=kwargs['mgroup_id'])
        context['form'] = GMaterialsForm(instance=context['value'])
        context['update'] = True
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        #return super(GMaterialsUpdate, self).dispatch(request, *args, **kwargs)

class GMaterialsDelete(DeleteView):
    model = GroupMaterials
    slug_field = 'mgroup_id'
    slug_url_kwarg = 'mgroup_id'
    success_url = reverse_lazy('gmaterials_list')
    template_name = 'home/crud/gmaterials_del.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GMaterialsDelete, self).dispatch(request, *args, **kwargs)

class DetailsGMaterials(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            if request.is_ajax():
                try:
                    if 'listMaterials' in request.GET:
                        context['details'] = [
                                            {
                                            'code': x.materials_id,
                                            'name': x.materials.matnom,
                                            'meter': x.materials.matmed,
                                            'unit': x.materials.unidad.uninom,
                                            'quantity': x.quantity
                                            }
                                            for x in DetailsGroup.objects.filter(mgroup_id=kwargs['mgroup']).order_by('materials__matnom')]
                        context['status'] = True
                    if 'searchGruop' in request.GET:
                        if request.GET.get('name') == 'gcode':
                            details = GroupMaterials.objects.filter(pk=request.GET.get('val'))
                        elif request.GET.get('name') == 'gdesc':
                            details = GroupMaterials.objects.filter(description__icontains=request.GET.get('val'))
                        context['details'] =[
                                            {
                                            'mgroup_id': x.mgroup_id,
                                            'desc': x.description,
                                            'materials': '%s %s'%(x.materials.matnom, x.materials.matmed),
                                            'parent': x.parent,
                                            'tgroup': x.tgroup.typeg
                                            }
                                            for x in details]
                        # print details, 'details'
                        context['status'] = True
                    if 'listDetails' in request.GET:
                        context['details'] = [
                                            {
                                            'code': x.materials_id,
                                            'name': x.materials.matnom,
                                            'meter': x.materials.matmed,
                                            'unit': x.materials.unidad.uninom,
                                            'quantity': x.quantity
                                            }
                                            for x in DetailsGroup.objects.filter(mgroup_id=request.GET.get('code')).order_by('materials__matnom')]
                        context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e.__str__()
                    context['status'] = False
                return self.render_to_json_response(context)
            context['mgroup'] = get_object_or_404(GroupMaterials, mgroup_id=kwargs['mgroup'])
            context['gmaterials'] = DetailsGroup.objects.filter(mgroup_id=kwargs['mgroup']).order_by('materials__matnom')
            # print kwargs['mgroup']
            return render_to_response('home/crud/detailsgmaterials.html', context, context_instance=RequestContext(request))
        except TemplateDoesNotExist, e:
            raise Http404('Template Does Not Exist')

    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'addMaterials' in request.POST:
                    try:
                        dt = DetailsGroup.objects.get(mgroup_id=kwargs['mgroup'], materials_id=request.POST.get('code'))
                        dt.quantity = (dt.quantity + float(request.POST.get('quantity')))
                        dt.save()
                    except ObjectDoesNotExist:
                        nw = DetailsGroup()
                        nw.mgroup_id = kwargs['mgroup']
                        nw.materials_id = request.POST.get('code')
                        nw.quantity = request.POST.get('quantity')
                        nw.save()
                    context['status'] = True
                if 'eMaterials' in request.POST:
                    dt = DetailsGroup.objects.get(mgroup_id=kwargs['mgroup'], materials_id=request.POST.get('code'))
                    dt.quantity = float(request.POST.get('quantity'))
                    dt.save()
                    context['status'] = True
                if 'delMaterial' in request.POST:
                    DetailsGroup.objects.get(mgroup_id=kwargs['mgroup'],materials_id=request.POST.get('materials')).delete()
                    context['status'] = True
                if 'delall' in request.POST:
                    DetailsGroup.objects.filter(mgroup_id=kwargs['mgroup']).delete()
                    context['status'] = True
                if 'copyClipboard' in request.POST:
                    if json.loads(request.POST.get('replace')):
                        DetailsGroup.objects.filter(mgroup_id=kwargs['mgroup']).delete()
                    for x in json.loads(request.POST.get('details')):
                        try:
                            dt = DetailsGroup.objects.get(mgroup_id=kwargs['mgroup'], materials_id=x['materials'])
                            dt.quantity = (dt.quantity + float(x['quantity']))
                            dt.save()
                        except ObjectDoesNotExist:
                            nw = DetailsGroup()
                            nw.mgroup_id = kwargs['mgroup']
                            nw.materials_id = x['materials']
                            nw.quantity = x['quantity']
                            nw.save()
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

class MaterialsKeep(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'code' in request.GET:
                    context['list'] = [
                    {
                        'materials': x.materiales_id,
                        'name': x.matnom,
                        'measure': x.matmed,
                        'unit': x.unidad.uninom,
                        'finished': x.matacb,
                        'area': x.matare
                    }
                    for x in Materiale.objects.filter(materiales_id__startswith=request.GET.get('code'))
                    ]
                    context['status'] = True
                if 'desc' in request.GET:
                    context['list'] = [
                    {
                        'materials': x.materiales_id,
                        'name': x.matnom,
                        'measure': x.matmed,
                        'unit': x.unidad.uninom,
                        'finished': x.matacb,
                        'area': x.matare
                    }
                    for x in Materiale.objects.filter(matnom__icontains=request.GET.get('desc'))
                    ]
                    context['status'] = True
                # Ajax method for json
                if 'searchName' in request.GET:
                    name = Materiale.objects.filter(matnom__icontains=request.GET['name']).distinct('matnom').order_by('matnom')
                    context['names'] = [
                        {
                            'name': x.matnom
                        }
                        for x in name
                    ]
                    context['status'] = True
                if 'searchNamebyCode' in request.GET:
                    name = Materiale.objects.filter(materiales_id=request.GET['scode'])
                    context['names'] = [
                        {
                            'name': x.matnom
                        }
                        for x in name
                    ]
                    context['status'] = True
                if 'searchMeter' in request.GET:
                    meter = Materiale.objects.filter(matnom__icontains=request.GET['name']).distinct('matmed').order_by('matmed')
                    context['meter'] = [
                        {
                            'measure': x.matmed,
                            'code': x.materiales_id
                        }
                        for x in meter
                    ]
                    context['status'] = True
                if 'summary' in request.GET:
                    material = Materiale.objects.get(materiales_id=request.GET['scode'])
                    price = None
                    try:
                        price = DetCompra.objects.filter(materiales_id=material.materiales_id).latest('compra__registrado').precio
                    except ObjectDoesNotExist, e:
                        price = 0
                    context['summary'] = {
                        'materials' : material.materiales_id,
                        'name': material.matnom,
                        'measure': material.matmed,
                        'unit': material.unidad.uninom,
                        'price': price
                    }
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)
        else:
            try:
                context['materials'] = Materiale.objects.all().order_by('matnom')[:50]
                context['unidad'] = Unidade.objects.all()
                return render_to_response('home/crud/materials.html', context, context_instance=RequestContext(request))
            except TemplateDoesNotExist, e:
                raise Http404(e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if 'exists' in request.POST:
                    obj = Materiale.objects.get(pk=request.POST.get('materiales_id'))
                    if obj:
                        context['status'] = True
                    else:
                        context['status'] = False
                if 'saveMaterial' in request.POST:
                    if 'edit' in request.POST:
                        obj = Materiale.objects.get(pk=request.POST.get('materiales_id'))
                        form = MaterialsForm(request.POST, instance=obj)
                    else:
                        form = MaterialsForm(request.POST)
                    if form.is_valid():
                        form.save()
                        context['status'] = True
                    else:
                        context['status'] = False
                if 'delete' in request.POST:
                    obj = Materiale.objects.get(pk=request.POST.get('materials'))
                    obj.delete()
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

class UnitAdd(CreateView):
    model = Unidade
    form_class = addUnidadeForm
    template_name = 'home/crud/unitadd.html'
    success_url = reverse_lazy('unit_add')

    def form_valid(self, form):
        if not self.model.objects.filter(unidad_id__istartswith=form.instance.uninom.upper()).count():
            form.instance.unidad_id = form.instance.uninom
            form.instance.uninom = form.instance.uninom.upper()
        else:
            context = dict()
            context['status'] = False
            context['raise'] = 'Error ya existe.'
            return render(self.request ,self.template_name, context)
        return super(UnitAdd, self).form_valid(form)

    def form_invalid(self, form):
        context = dict()
        context['status'] = False
        context['raise'] = 'Error al Guardar cambios, %s'%form
        return HttpResponse(simplejson.dumps(context), mimetype='application/json')

class Unit(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            if 'list' in request.GET:
                context['unit'] = list(Unidade.objects.filter(flag=True).values('unidad_id', 'uninom').order_by('uninom'))
                context['status'] = True
        except ObjectDoesNotExist, e:
            context['raise'] = str(e)
            context['status'] = False
        return self.render_to_json_response(context)

class ManPower(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            if request.is_ajax():
                try:
                    if 'listcbo' in request.GET:
                        context['list'] = list(Cargo.objects.values('cargo_id','cargos').filter(flag=True).order_by('cargos'))
                        context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = str(e)
                    context['status'] = False
                return self.render_to_json_response(context)
            if kwargs['add']:
                return render(request, 'home/crud/manpower_form.html', context)
            else:
                return render(request, 'home/crud/manpower.html')
        except TemplateDoesNotExist, e:
            raise Http404

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        #if request.is_ajax():
        #try:
        #    pass
        #except ObjectDoesNotExist, e:
        #    context['raise'] = str(e)
            #context['status'] = False
        #return self.render_to_json_response(context)
        if kwargs['add']:
            try:
                ob = Cargo()
                ob.cargo_id = request.POST['manpower']
                ob.cargos = request.POST['name']
                ob.area = request.POST['area']
                ob.flag = True
                ob.save()
            except ObjectDoesNotExist, e:
                raise
            return render(request, 'home/crud/manpower.html')
