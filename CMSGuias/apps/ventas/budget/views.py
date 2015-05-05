#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
#import datetime
#import os

from django.db.models import Q, Count, Sum
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
# from django.contrib.auth.mod import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils import simplejson, timezone
from django.utils.decorators import method_decorator
from django.template import RequestContext, TemplateDoesNotExist
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import UpdateView, CreateView
from decimal import Decimal

from .models import *
from .forms import *
from CMSGuias.apps.home.models import Unidade
from CMSGuias.apps.tools import genkeys

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
        return simplejson.dumps(context, encoding='utf-8', cls=DjangoJSONEncoder)

class addAnalysisGroup(CreateView):
    model = AnalysisGroup
    form_class = addAnalysisGroupForm
    template_name = 'budget/addanalysisgroup.html'
    success_url = reverse_lazy('addanalysisgroup')

    def form_valid(self, form):
        if not self.model.objects.filter(name=form.instance.name.upper()).count():
            form.instance.agroup_id = genkeys.generateGroupAnalysis()
            form.instance.name = form.instance.name.upper()
        else:
            context = dict()
            context['status'] = False
            context['raise'] = 'Error ya existe.'
            return render(self.request ,self.template_name, context)
        return super(addAnalysisGroup, self).form_valid(form)

    def form_invalid(self, form):
        context = dict()
        context['status'] = False
        context['raise'] = 'Error al Guardar cambios, %s'%form
        return HttpResponse(simplejson.dumps(context), mimetype='application/json')

class AnalysisGroupList(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'list' in request.GET:
                    context['list'] = list(AnalysisGroup.objects.filter(flag=True).values('agroup_id', 'name').order_by('name'))
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = str(e)
                context['status'] = False
                print context
            return self.render_to_json_response(context)

class AnalystPrices(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'list' in request.GET:
                    analysis = None
                    if 'name' in request.GET:
                        analysis = Analysis.objects.filter(name__istartswith=request.GET['name']).order_by('name')
                    if 'code' in request.GET:
                        analysis = Analysis.objects.filter(pk=request.GET['code'])
                    if 'group' in request.GET:
                        analysis = Analysis.objects.filter(group_id=request.GET['group']).order_by('name')
                    if analysis:
                        context['analysis'] = [
                            {
                                'code': x.analysis_id,
                                'name': x.name,
                                'unit': x.unit.uninom,
                                'performance': x.performance,
                                'group': x.group.name
                            }
                            for x in analysis
                        ]
                        context['status'] = True
                    else:
                        context['status'] = False
                        context['raise'] = 'No se han encontrado resultados para la busqueda.'
            except ObjectDoesNotExist, e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
        context['analysis'] = Analysis.objects.filter(flag=True).order_by('-register')
        context['unit'] = Unidade.objects.filter(flag=True)
        context['group'] = AnalysisGroup.objects.filter(flag=True)
        return render(request, 'budget/analysis.html', context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                # Save new Analysis
                if 'analysisnew' in request.POST:
                    an = Analysis()
                    form = addAnalysisForm(request.POST)
                    if form.is_valid():
                        add = form.save(commit=False)
                        key = genkeys.generateAnalysis()
                        add.analysis_id = key
                        add.flag = True
                        add.save()
                        context['key'] = key
                        context['status'] = True
                    else:
                        context['status'] = False
                        context['raise'] = 'Error de Fields invalid.'
            except ObjectDoesNotExist, e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)

class AnalysisDetails(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            context = dict()
            if request.is_ajax():
                try:
                    # Transaction Materials
                    if 'listMaterials' in request.GET:
                        context['materials'] = [
                            {
                                'pk': x.id,
                                'code': x.materials_id,
                                'name': '%s - %s'%(x.materials.matnom,x.materials.matmed),
                                'unit': x.materials.unidad.uninom,
                                'price': x.price,
                                'quantity': x.quantity,
                                'partial': x.partial
                            }
                            for x in APMaterials.objects.filter(analysis_id=kwargs['analysis']).order_by('materials__matnom')
                        ]
                        context['status'] = True
                    if 'listManPower' in request.GET:
                        context['manpower'] = [
                            {
                                'id': x.id,
                                'code': x.manpower_id,
                                'name': x.manpower.cargos,
                                'unit': x.manpower.unit.uninom,
                                'gang': x.gang,
                                'quantity': x.quantity,
                                'price': x.price,
                                'partial': float(x.partial)
                            }
                            for x in APManPower.objects.filter(analysis_id=kwargs['analysis']).order_by('manpower__cargos')
                        ]
                        context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = str(e)
                    context['status'] = False
                return self.render_to_json_response(context)
            context['analysis'] = Analysis.objects.get(analysis_id=kwargs['analysis'])
            context['materials'] = APMaterials.objects.filter(analysis_id=kwargs['analysis']).order_by('materials__matnom')
            context['manpower'] = APManPower.objects.filter(analysis_id=kwargs['analysis']).order_by('manpower__cargos')
            # context['tools'] = APTools.objects.filter(analysis_id=kwargs['analysis']).order_by()
            return render(request, 'budget/analysisdetails.html', context)
        except TemplateDoesNotExist, e:
            raise Http404(e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                # block keep Materials
                if 'addMaterials' in request.POST:
                    try:
                        em = APMaterials.objects.get(
                            analysis_id=kwargs['analysis'],
                            materials_id=request.POST.get('materials')
                        )
                        em.quantity += float(request.POST.get('quantity'))
                        em.price = request.POST.get('price')
                        em.save()
                    except ObjectDoesNotExist:
                        add = APMaterials()
                        add.analysis_id = kwargs['analysis']
                        add.materials_id = request.POST['materials']
                        add.quantity = request.POST['quantity']
                        add.price = request.POST['price']
                        add.save()
                    context['status'] = True
                if 'editMaterials' in request.POST:
                    edit = APMaterials.objects.get(
                        analysis_id=kwargs['analysis'],
                        materials_id=request.POST.get('materials'),
                        id=request.POST.get('id')
                    )
                    edit.price = request.POST.get('price')
                    edit.quantity = request.POST.get('quantity')
                    edit.save()
                    context['status'] = True
                if 'delMaterials' in request.POST:
                    APMaterials.objects.get(analysis_id=kwargs['analysis'], materials_id=request.POST.get('materials'), id=request.POST.get('id')).delete()
                    context['status'] = True
                if 'delMaterialsAll' in request.POST:
                    APMaterials.objects.filter(analysis_id=kwargs['analysis']).delete()
                    context['status'] = True
                # block end
                if 'addTools' in request.POST:
                    context['status'] = True
                if 'editTools' in request.POST:
                    context['status'] = True
                if 'delTools' in request.POST:
                    context['status'] = True
                if 'addMan' in request.POST:
                    try:
                        em = APManPower.objects.get(
                            analysis_id=kwargs['analysis'],
                            manpower_id=request.POST.get('manpower')
                        )
                        em.gang = float(request.POST['gang'])
                        em.price = float(request.POST.get('price'))
                        em.quantity = ((float(request.POST['gang']) * 8)/ float(request.POST['performance']))
                        em.save()
                    except ObjectDoesNotExist:
                        add = APManPower()
                        add.analysis_id = kwargs['analysis']
                        add.manpower_id = request.POST['manpower']
                        add.gang = float(request.POST['gang'])
                        add.price = float(request.POST['price'])
                        add.quantity = ((float(request.POST['gang']) * 8)/ float(request.POST['performance']))
                        add.save()
                    context['status'] = True
                if 'editMan' in request.POST:
                    context['status'] = True
                if 'delMan' in request.POST:
                    APManPower.objects.get(analysis_id=kwargs['analysis'], manpower_id=request.POST['manpower']).detele()
                    context['status'] = True
                if 'delManPowerAll' in request.POST:
                    APManPower.objects.filter(analysis_id=kwargs['analysis']).delete()
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)