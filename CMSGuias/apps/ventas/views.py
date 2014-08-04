#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime

from django.db.models import Q, Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# from django.contrib.auth.mod import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404,get_object_or_404
from django.utils import simplejson, timezone
from django.utils.decorators import method_decorator
from django.template import RequestContext, TemplateDoesNotExist
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import UpdateView, CreateView

from CMSGuias.apps.home.models import *
from CMSGuias.apps.operations.models import MetProject
from CMSGuias.apps.almacen.models import Inventario
from .models import *
from .forms import *
from CMSGuias.apps.tools import genkeys, globalVariable, uploadFiles


## Class Bases Views Generic

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

# View home Sales
class SalesHome(TemplateView):
    template_name = "sales/home.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SalesHome, self).dispatch(request, *args, **kwargs)

# View list project
class ProjectsList(JSONResponseMixin, TemplateView):
    template_name = "sales/projects.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = super(ProjectsList, self).get_context_data(**kwargs)
        try:
            context['list'] = Proyecto.objects.filter(Q(flag=True), ~Q(status='DA'))
            context['country'] = Pais.objects.filter(flag=True)
            context['customers'] = Cliente.objects.filter(flag=True)
            return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        except TemplateDoesNotExist, e:
            messages.error(request, "Template Does Not Exist %s"%e)
            raise Http404("Template Does Not Exist %s"%e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if request.POST.get('type') == 'new':
                    form = ProjectForm(request.POST)
                    key = genkeys.GenerateIdPorject()
                    print form, form.is_valid(), request.user.get_profile().empdni_id, key
                    if form.is_valid():
                        add = form.save(commit=False)
                        add.proyecto_id = key
                        # add.empdni_id = request.user.get_profile().empdni_id
                        add.status = 'PE'
                        add.save()
                        context['status'] = True
                    else:
                        context['status'] = False
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

# add sectors
class SectorsView(JSONResponseMixin, View):
    template_name = 'sales/crud/sectors_form.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                obj = Sectore.objects.filter(proyecto_id=request.GET.get('pro'), subproyecto_id=request.GET.get('sub') if request.GET.get('sub') != '' else None).order_by('subproyecto','planoid')
                context['list'] =[{'sector_id': x.sector_id, 'nomsec': x.nomsec, 'planoid' : x.planoid} for x in obj]
                context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)
        context['pro'] = request.GET.get('pro')
        context['sub'] = request.GET.get('sub')
        if request.GET.get('type') == 'update':
            obj = Sectore.objects.get(proyecto_id=request.GET.get('pro'), subproyecto_id=request.GET.get('sub') if request.GET.get('sub') != '' else None, sector_id=request.GET.get('sec'))
            context['form'] = SectoreForm(instance=obj)
            context['type'] = 'update'
        elif request.GET.get('type') == 'new':
            context['form'] = SectoreForm
            context['type'] = 'new'
        return render_to_response(self.template_name, context, context_instance = RequestContext(request))

    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            if request.POST.get('type') == 'update':
                obj = Sectore.objects.get(proyecto_id=request.POST.get('proyecto'), subproyecto_id=request.POST.get('sub') if request.POST.get('subproyecto') != '' else None, sector_id=request.POST.get('sector_id'))
                form = SectoreForm(request.POST, instance=obj)
                print form, form.is_valid()
                if form.is_valid():
                    form.save()
                    context['status'] = True
                    context['msg'] = 'success'
                else:
                    context['status'] = False
                    context['msg'] = 'error'
            elif request.POST.get('type') == 'new':
                form = SectoreForm(request.POST)
                if form.is_valid():
                    add = form.save(commit=False)
                    id = "%s%s"%(add.proyecto_id, add.sector_id)
                    print id, len(id)
                    add.sector_id = id
                    add.save()
                    context['status'] = True
                    context['msg'] = 'success'
                else:
                    context['status'] = False
                    context['msg'] = 'error'
        except ObjectDoesNotExist, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return render_to_response(self.template_name, context, context_instance = RequestContext(request))

# Add Subproject
class SubprojectsView(JSONResponseMixin, View):
    template_name = 'sales/crud/subprojects_form.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['pro'] = request.GET.get('pro')
        if request.GET.get('type') == 'update':
            obj = Subproyecto.objects.get(proyecto_id=request.GET.get('pro'), subproyecto_id=request.GET.get('sub'))
            context['form'] = SubprojectForm(instance=obj)
            context['type'] = 'update'
        elif request.GET.get('type') == 'new':
            context['form'] = SubprojectForm
            context['type'] = 'new'
        return render_to_response(self.template_name, context, context_instance = RequestContext(request))

    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            if request.POST.get('type') == 'update':
                obj = Subproyecto.objects.get(proyecto_id=request.POST.get('proyecto'),subproyecto_id=request.POST.get('subproyecto_id'))
                form = SubprojectForm(request.POST, instance=obj)
                print form, form.is_valid()
                if form.is_valid():
                    form.save()
                    context['status'] = True
                    context['msg'] = 'success'
                else:
                    context['status'] = False
                    context['msg'] = 'error'
            elif request.POST.get('type') == 'new':
                form = SubprojectForm(request.POST)
                print form, form.is_valid()
                if form.is_valid():
                    form.save()
                    context['status'] = True
                    context['msg'] = 'success'
                else:
                    context['status'] = False
                    context['msg'] = 'error'
        except ObjectDoesNotExist, e:
            context['raise'] = e.__str__()
            context['status'] = False
        return render_to_response(self.template_name, context, context_instance = RequestContext(request))

# Manager View Project
class ProjectManager(JSONResponseMixin, View):
    template_name = 'sales/managerpro.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            """if request.is_ajax():
            if 'list' in request.GET:
                try:
                    context['alerts'] = [{'id':x.id, 'date': globalVariable.format_date_str(x.registrado,'%d de %B de %Y'), 'time':globalVariable.format_time_str(_date=x.registrado,options={'tz':True}), 'name': x.empdni.name_complete, 'charge':x.charge.area, 'message': mark_safe(escape(x.message)), 'status': x.status } for x in Alertasproyecto.objects.filter(Q(proyecto_id=kwargs['project']) | ~Q(subproyecto_id=None) | Q(subproyecto_id=None), Q(sector_id=None), Q(flag=True)).order_by('-registrado')]
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e.__str__()
                    context['status'] = False
                return self.render_to_json_response(context)"""
            context['project'] = Proyecto.objects.get(pk=kwargs['project'])
            context['subpro'] = Subproyecto.objects.filter(proyecto_id=kwargs['project'])
            context['sectors'] = Sectore.objects.filter(proyecto_id=kwargs['project']).order_by('subproyecto','planoid')
            context['operation'] = Employee.objects.filter(charge__area__istartswith='opera').order_by('charge__area')
            context['admin'] = Employee.objects.filter(charge__area__istartswith='admin').order_by('charge__area')
            context['alerts'] = Alertasproyecto.objects.filter(Q(proyecto_id=kwargs['project']) | ~Q(subproyecto_id=None), Q(sector_id=None), Q(flag=True)).order_by('-registrado')
            return render_to_response(self.template_name, context, context_instance = RequestContext(request))
        except TemplateDoesNotExist, e:
            messages.error(request, 'Template not Exist %s',e)
            raise Http404('Page Not Found')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            if request.POST.get('type') == 'files':
                try:
                    # charge file to server
                    if request.POST.get('sub') == '':
                        admin = '/storage/projects/%s/administrative/'%(request.POST.get('pro'))
                        opera = '/storage/projects/%s/operation/'%(request.POST.get('pro'))
                    else:
                        admin = '/storage/projects/%s/%s/administrative/'%(request.POST.get('pro'), request.POST.get('sub'))
                        opera = '/storage/projects/%s/%s/operation/'%(request.POST.get('pro'), request.POST.get('sub'))

                    if 'administrative' in request.FILES:
                        fileadmin = uploadFiles.upload(admin, request.FILES['administrative'], {'name': 'admin'})
                        # descompress files in the server
                        context['descompress'] =  uploadFiles.descompressRAR(fileadmin, admin)
                        # delete files temp
                        uploadFiles.removeTmp(fileadmin)
                    if 'operation' in request.FILES:
                        fileopera = uploadFiles.upload(opera, request.FILES['operation'], {'name': 'opera'})
                        # descompress files in the server
                        context['descompress'] = uploadFiles.descompressRAR(fileopera, opera)
                        # delete files temp
                        uploadFiles.removeTmp(fileopera)
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    print e
                    context['raise'] = e.__str__()
                    context['status'] = False

            if request.POST.get('type') == 'add':
                form = AlertasproyectoForm(request.POST)
                if form.is_valid():
                    add = form.save(commit=False)
                    add.empdni_id = request.user.get_profile().empdni_id
                    add.charge_id = request.user.get_profile().empdni.charge_id
                    add.save()
                    context['status'] = True
                else:
                    context['status'] = False
            if request.POST.get('type') == 'edit':
                obj = Alertasproyecto.objects.get(pk=request.POST.get('edit'))
                form = AlertasproyectoForm(request.POST, instance=obj)
                if form.is_valid():
                    form.save()
                    context['status'] = True
                else:
                    context['status'] = False
            if request.POST.get('type') == 'responsible':
                try:
                    user = userProfile.objects.get(empdni_id=request.POST.get('admin'))
                    # authenticate password admin
                    if user.user.check_password(request.POST.get('passwd')):
                        #if user.user.is_superuser:
                        pro = Proyecto.objects.get(pk=kwargs['project'])
                        pro.empdni_id = request.POST.get('responsible')
                        pro.save()
                        context['status'] = True
                    else:
                        context['raise'] = 'Password incorrect!'
                        context['status'] = False
                except ObjectDoesNotExist, e:
                    context['raise'] = e.__str__()
                    context['status'] = False
            if request.POST.get('type') == 'approved':
                # this function is for approve the project
                try:
                    user = userProfile.objects.get(empdni_id=request.POST.get('admin'))
                    # authenticate password admin
                    if user.user.check_password(request.POST.get('passwd')):
                        #if user.user.is_superuser:
                        pro = Proyecto.objects.get(pk=kwargs['project'])
                        pro.approved_id = request.POST.get('admin')
                        pro.status = 'AC'
                        print 'all correct'
                        pro.save()
                        sub = Subproyecto.objects.filter(proyecto_id=kwargs['project'])
                        if sub:
                            sub.update(status='AC')
                        sec = Sectore.objects.filter(proyecto_id=kwargs['project'])
                        if sec:
                            sec.update(status='AC')
                        # paste all list of materials to "MetProject"
                        for x in Metradoventa.objects.filter(proyecto_id=kwargs['project']):
                            obj = MetProject()
                            obj.proyecto_id = x.proyecto_id
                            obj.subproyecto_id = x.subproyecto_id
                            obj.sector_id = x.sector_id
                            obj.materiales_id = x.materiales_id
                            obj.cantidad = x.cantidad
                            obj.precio = x.precio
                            obj.brand_id = x.brand_id
                            obj.model_id = x.model_id
                            obj.save()
                        context['status'] = True
                    else:
                        context['raise'] = 'Password incorrect!'
                        context['status'] = False
                except ObjectDoesNotExist, e:
                    context['raise'] = e.__str__()
                    context['status'] = False
            return self.render_to_json_response(context)
# Manager View Sectors
class SectorManage(JSONResponseMixin, View):
    template_name = 'sales/managersec.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            if request.is_ajax():
                if 'type' in request.GET:
                    if request.GET.get('type') == 'list':
                        try:
                            obj = Metradoventa.objects.filter(proyecto_id=request.GET.get('pro'), subproyecto_id=request.GET.get('sub') if request.GET.get('sub') != '' else None, sector_id=request.GET.get('sec')).order_by('materiales__matnom')
                            context['list'] = [{'id':x.id,'materials_id': x.materiales_id, 'name': x.materiales.matnom, 'measure':x.materiales.matmed, 'unit': x.materiales.unidad.uninom, 'brand' : x.brand.brand, 'model' : x.model.model , 'quantity':x.cantidad, 'price':x.precio} for x in obj]
                            context['status'] = True
                        except ObjectDoesNotExist, e:
                            context['raise'] = e.__str__()
                            context['status'] = False
                return self.render_to_json_response(context)
            context['project'] = Proyecto.objects.get(pk=kwargs['pro'])
            if kwargs['sub'] != unicode(None):
                context['subproject'] = Subproyecto.objects.get(proyecto_id=kwargs['pro'], subproyecto_id=kwargs['sub'])
            context['sector'] = Sectore.objects.get(proyecto_id=kwargs['pro'], subproyecto_id=kwargs['sub'] if kwargs['sub'] != unicode(None) else None, sector_id=kwargs['sec'])
            context['planes'] = SectorFiles.objects.filter(proyecto_id=kwargs['pro'], subproyecto_id=kwargs['sub'] if kwargs['sub'] != unicode(None) else None, sector_id=kwargs['sec'])
            context['system'] = Configuracion.objects.get(periodo=globalVariable.get_year)
            context['currency'] = Moneda.objects.filter(flag=True).order_by('moneda')
            context['exchange'] = TipoCambio.objects.filter(fecha=globalVariable.date_now())
            if context['project'].status != 'AC':
                context['materials'] = Metradoventa.objects.filter(proyecto_id=kwargs['pro'], subproyecto_id=kwargs['sub'] if kwargs['sub'] != unicode(None) else None, sector_id=kwargs['sec']).order_by('materiales__matnom')
            else:
                met = MetProject.objects.filter(proyecto_id=kwargs['pro'], subproyecto_id=kwargs['sub'] if kwargs['sub'] != unicode(None) else None, sector_id=kwargs['sec']).order_by('materiales__matnom')
                data = list()
                for x in met:
                    stock = None
                    # get stock of Inventory
                    # if x.brand_id == 'BR000':
                    stock = Inventario.objects.filter(materiales_id=x.materiales_id, periodo=globalVariable.get_year)
                    data.append({'materiales_id':x.materiales_id, 'name':x.materiales.matnom,'measure':x.materiales.matmed,'unit':x.materiales.unidad.uninom,'brand':x.brand.brand, 'model':x.model.model,'quantity':x.cantidad,'price':x.precio, 'stock':stock[0].stock})
                context['meter'] = data
                print data
            return render_to_response(self.template_name, context, context_instance = RequestContext(request))
        except TemplateDoesNotExist, e:
            messages.error(request, 'Template not Exist %s',e)
            raise Http404('Page Not Found')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if 'type' in request.POST:
                    if request.POST.get('type') == 'plane':
                        form = SectorFilesForm(request.POST, request.FILES)
                        if form.is_valid():
                            form.save()
                        context['status'] = True
                    if request.POST.get('type') == 'delplane':
                        obj = SectorFiles.objects.get(proyecto_id=request.POST.get('pro'), subproyecto_id=request.POST.get('sub') if request.POST.get('sub') else None, sector_id=request.POST.get('sec'), files=request.POST.get('files'))
                        obj.delete()
                        uploadFiles.removeTmp('%s/%s'%(globalVariable.relative_path, request.POST.get('files')))
                        context['status'] = True
                    if request.POST.get('type') == 'add':
                        if 'edit' in request.POST:
                            obj = Metradoventa.objects.get(proyecto_id=request.POST.get('proyecto'), subproyecto_id=request.POST.get('subproyecto') if request.POST.get('subproyecto') else None, sector_id=request.POST.get('sector'), materiales_id=request.POST.get('materiales'))
                            form = MetradoventaForm(request.POST, instance=obj)
                        else:
                            form = MetradoventaForm(request.POST)
                        if form.is_valid():
                            if 'edit' in request.POST:
                                form.save()
                            else:
                                obj = Metradoventa.objects.filter(proyecto_id=request.POST.get('proyecto'), subproyecto_id=request.POST.get('subproyecto') if request.POST.get('subproyecto') else None, sector_id=request.POST.get('sector'), materiales_id=request.POST.get('materiales'))
                                if obj:
                                    obj.cantidad = obj[0].cantidad + float(request.POST.get('cantidad'))
                                    obj.precio = request.POST.get('precio')
                                    obj.save()
                                else:
                                    form.save()
                            context['status'] = True
                        else:
                            context['status'] = False
                    if request.POST.get('type') == 'del':
                        obj = Metradoventa.objects.filter(proyecto_id=request.POST.get('pro'), subproyecto_id=request.POST.get('sub') if request.POST.get('sub') else None, sector_id=request.POST.get('sec'), materiales_id=request.POST.get('materials'))
                        print obj.delete(), 'object delete'
                        context['status'] = True
                    if request.POST.get('type') == 'killdata':
                        obj = Metradoventa.objects.filter(proyecto_id=request.POST.get('pro'), subproyecto_id=request.POST.get('sub') if request.POST.get('sub') else None, sector_id=request.POST.get('sec'))
                        obj.delete()
                        context['status'] = True
                else:
                    context['status'] = False
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

