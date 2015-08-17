#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import json
# import datetime
# import os

# from django.db.models import Q, Count, Sum
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse_lazy
from django.core import serializers
# from django.contrib import messages
# from django.contrib.auth.mod import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.template import TemplateDoesNotExist
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
# from decimal import Decimal

from .models import *
from .forms import *
from CMSGuias.apps.home.models import Unidade, Moneda, Cliente
from CMSGuias.apps.tools import genkeys

# Class Bases Views Generic


class JSONResponseMixin(object):

    def render_to_json_response(self, context, **response_kwargs):
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            mimetype='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        return simplejson.dumps(
            context, encoding='utf-8', cls=DjangoJSONEncoder)


class addAnalysisGroup(CreateView):
    model = AnalysisGroup
    form_class = addAnalysisGroupForm
    template_name = 'budget/addanalysisgroup.html'
    success_url = reverse_lazy('addanalysisgroup')

    def form_valid(self, form):
        count = self.model.objects.filter(
            name=form.instance.name.upper()).count()
        if not count:
            form.instance.agroup_id = genkeys.generateGroupAnalysis()
            form.instance.name = form.instance.name.upper()
        else:
            context = dict()
            context['status'] = False
            context['raise'] = 'Error ya existe.'
            return render(
                self.request, self.template_name, context)
        return super(addAnalysisGroup, self).form_valid(form)

    def form_invalid(self, form):
        context = dict()
        context['status'] = False
        context['raise'] = 'Error al Guardar cambios, %s' % form
        return HttpResponse(
            simplejson.dumps(context), mimetype='application/json')


class AnalysisGroupList(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'list' in request.GET:
                    context['list'] = list(
                        AnalysisGroup.objects.filter(flag=True).values(
                            'agroup_id', 'name').order_by('name'))
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
                        analysis = Analysis.objects.filter(
                            name__istartswith=request.GET['name']
                        ).order_by('name')
                    if 'code' in request.GET:
                        analysis = Analysis.objects.filter(
                            pk=request.GET['code'])
                    if 'group' in request.GET:
                        analysis = Analysis.objects.filter(
                            group_id=request.GET['group']).order_by('name')
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
                        context['raise'] = ('No se han encontrado resultados'
                                            + ' para la busqueda.')
            except ObjectDoesNotExist, e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
        context['analysis'] = Analysis.objects.filter(
            flag=True).order_by('-register')
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
                    # an = Analysis()
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
                if 'edit' in request.POST:
                    ed = Analysis.objects.get(
                        analysis_id=request.POST['analysis_id'])
                    performance = ed.performance
                    form = addAnalysisForm(request.POST, instance=ed)
                    if form.is_valid():
                        # Change details analysis manpower and tools
                        if performance != float(request.POST['performance']):
                            apm = APManPower.objects.filter(
                                analysis_id=request.POST['analysis_id'])
                            for x in apm:
                                x.quantity = (
                                    (float(x.gang) * 8)
                                    / float(request.POST['performance']))
                                x.save()
                            apt = APTools.objects.filter(
                                analysis_id=request.POST['analysis_id'])
                            for x in apt:
                                x.quantity = (
                                    (float(x.gang) * 8)
                                    / float(request.POST['performance']))
                                x.save()
                        form.save()
                        context['status'] = True
                    else:
                        context['status'] = False
                        context['raise'] = 'Error de Fields invalid.'
                if 'delAnalysis' in request.POST:
                    analysis = Analysis.objects.get(
                        analysis_id=request.POST['analysis'])
                    APMaterials.objects.filter(
                        analysis_id=request.POST['analysis']).delete()
                    APManPower.objects.filter(
                        analysis_id=request.POST['analysis']).delete()
                    APTools.objects.filter(
                        analysis_id=request.POST['analysis']).delete()
                    analysis.delete()
                    context['status'] = True
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
                                'name': '%s - %s' % (
                                    x.materials.matnom, x.materials.matmed),
                                'unit': x.materials.unidad.uninom,
                                'price': x.price,
                                'quantity': x.quantity,
                                'partial': x.partial
                            }
                            for x in APMaterials.objects.filter(
                                analysis_id=kwargs['analysis']
                            ).order_by('materials__matnom')
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
                            for x in APManPower.objects.filter(
                                analysis_id=kwargs['analysis']
                            ).order_by('manpower__cargos')
                        ]
                        context['status'] = True
                    if 'listTools' in request.GET:
                        context['tools'] = [
                            {
                                'id': x.id,
                                'code': x.tools_id,
                                'name': '%s - %s' % (
                                    x.tools.name, x.tools.measure),
                                'unit': x.tools.unit.uninom,
                                'gang': x.gang,
                                'quantity': x.quantity,
                                'price': x.price,
                                'partial': float(x.partial)
                            }
                            for x in APTools.objects.filter(
                                analysis_id=kwargs['analysis']
                            ).order_by('tools__name')
                        ]
                        context['status'] = True
                    if 'priceAll' in request.GET:
                        context['total'] = Analysis.objects.get(
                            analysis_id=kwargs['analysis']).total
                        context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = str(e)
                    context['status'] = False
                return self.render_to_json_response(context)
            context['analysis'] = Analysis.objects.get(
                analysis_id=kwargs['analysis'])
            context['materials'] = APMaterials.objects.filter(
                analysis_id=kwargs['analysis']
            ).order_by('materials__matnom')
            context['manpower'] = APManPower.objects.filter(
                analysis_id=kwargs['analysis']
            ).order_by('manpower__cargos')
            context['tools'] = APTools.objects.filter(
                analysis_id=kwargs['analysis']
            ).order_by('tools__name')
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
                    APMaterials.objects.get(
                        analysis_id=kwargs['analysis'],
                        materials_id=request.POST.get('materials'),
                        id=request.POST.get('id')).delete()
                    context['status'] = True
                if 'delMaterialsAll' in request.POST:
                    APMaterials.objects.filter(
                        analysis_id=kwargs['analysis']).delete()
                    context['status'] = True
                if 'addTools' in request.POST:
                    try:
                        em = APTools.objects.get(
                            analysis_id=kwargs['analysis'],
                            tools_id=request.POST.get('tools')
                        )
                        em.gang = float(request.POST['gang'])
                        em.price = float(request.POST['price'])
                        em.quantity = (
                            (float(request.POST['gang']) * 8)
                            / float(request.POST['performance'])
                        )
                        em.save()
                    except ObjectDoesNotExist, e:
                        add = APTools()
                        add.analysis_id = kwargs['analysis']
                        add.tools_id = request.POST['tools']
                        add.gang = float(request.POST['gang'])
                        add.price = float(request.POST['price'])
                        add.quantity = (
                            (float(request.POST['gang']) * 8)
                            / float(request.POST['performance']))
                        add.save()
                    context['status'] = True
                if 'delToolsAll' in request.POST:
                    APTools.objects.filter(
                        analysis_id=kwargs['analysis']).delete()
                    context['status'] = True
                if 'delTools' in request.POST:
                    APTools.objects.filter(
                        analysis_id=kwargs['analysis'],
                        tools_id=request.POST['tools']).delete()
                    context['status'] = True
                if 'addMan' in request.POST:
                    try:
                        em = APManPower.objects.get(
                            analysis_id=kwargs['analysis'],
                            manpower_id=request.POST.get('manpower')
                        )
                        em.gang = float(request.POST['gang'])
                        em.price = float(request.POST.get('price'))
                        em.quantity = (
                            (float(request.POST['gang']) * 8)
                            / float(request.POST['performance']))
                        em.save()
                    except ObjectDoesNotExist:
                        add = APManPower()
                        add.analysis_id = kwargs['analysis']
                        add.manpower_id = request.POST['manpower']
                        add.gang = float(request.POST['gang'])
                        add.price = float(request.POST['price'])
                        add.quantity = (
                            (float(request.POST['gang']) * 8)
                            / float(request.POST['performance']))
                        add.save()
                    context['status'] = True
                if 'editMan' in request.POST:
                    context['status'] = True
                if 'delMan' in request.POST:
                    APManPower.objects.get(
                        analysis_id=kwargs['analysis'],
                        manpower_id=request.POST['manpower']).delete()
                    context['status'] = True
                if 'delManPowerAll' in request.POST:
                    APManPower.objects.filter(
                        analysis_id=kwargs['analysis']).delete()
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)

# Budget View


class BudgetView(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                pass
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
        else:
            try:
                context['currency'] = Moneda.objects.filter(flag=True)
                context['customer'] = Cliente.objects.filter(flag=True)
                # context['country'] = Pais.objects.filter(flag=True)
                context['budget'] = Budget.objects.filter(
                    flag=True, status='PE').order_by('-register')
                return render(request, 'budget/budget.html', context)
            except TemplateDoesNotExist as e:
                raise Http404(e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            if 'saveBudget' in request.POST:
                if 'editbudget' in request.POST:
                    form = addBudgetForm(
                        request.POST, instance=Budget.objects.get(
                            budget_id=request.GET['budget']))
                else:
                    form = addBudgetForm(request.POST)
                if form.is_valid():
                    if 'editbudget' in request.POST:
                        form.save()
                    else:
                        add = form.save(commit=False)
                        key = genkeys.generateBudget()
                        add.budget_id = key
                        add.version = 'RV001'
                        add.save()
                    context['id'] = key
                    context['status'] = True
                else:
                    context['status'] = False
                    context['raise'] = 'Campos incorrectos!'
        except ObjectDoesNotExist as e:
            context['raise'] = str(e)
            context['status'] = False
        return self.render_to_json_response(context)


class BudgetItemsView(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            if request.is_ajax():
                try:
                    if 'budgetData' in request.GET:
                        budget = Budget.objects.get(
                            budget_id=kwargs['budget'])
                        context['budget'] = {
                            'budget_id': budget.budget_id,
                            'revision': budget.version,
                            'name': budget.name,
                            'customers': budget.customers.razonsocial,
                            'address': budget.address,
                            'country': budget.country.paisnom,
                            'departament': budget.departament.depnom,
                            'province': budget.province.pronom,
                            'district': budget.district.distnom,
                            'register': budget.register,
                            'hourwork': budget.hourwork,
                            'finish': budget.finish,
                            'currency': budget.currency.moneda,
                            'observation': budget.observation}
                        context['status'] = True
                    if 'listItems' in request.GET:
                        oitems = BudgetItems.objects.filter(
                            budget_id=request.GET['budget']).order_by('item')
                        context['items'] = [
                            {
                                'item': x.item,
                                'version': x.budget.version,
                                'budget': x.budget_id,
                                'budgeti': x.budgeti_id,
                                'name': x.name,
                                'base': x.base,
                                'offer': x.offer,
                                'register': x.register.strftime('%Y-%m-%d'),
                                'tag': x.tag
                            }
                            for x in oitems
                        ]
                        context['status'] = True
                except ObjectDoesNotExist as e:
                    context['raise'] = str(e)
                    context['status'] = False
                return self.render_to_json_response(context)
            # context = kwargs
            return render(request, 'budget/budgetitems.html', context)
        except TemplateDoesNotExist as e:
            raise Http404(e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'saveItemBudget' in request.POST:
                    if 'editItem' in request.POST:
                        form = addItemBudgetForm(
                            request.POST,
                            instance=BudgetItems.objects.get(
                                budget_id=kwargs['budget'],
                                budgeti_id=request.POST['budgeti'] if 'budgeti' in request.POST else request.POST['budget_id'] + '001'))
                    else:
                        form = addItemBudgetForm(request.POST)
                    if form.is_valid():
                        add = form.save(commit=False)
                        if 'editItem' not in request.POST:
                            add.budget_id = request.POST['budget_id']
                            add.item = (
                                BudgetItems.objects.filter(
                                    budget_id=request.POST['budget_id']
                                ).count() + 1
                            )
                            add.budgeti_id = ('%s%s' % (
                                request.POST['budget_id'],
                                '{:0>3d}'.format(add.item)))
                        add.save()
                        context['status'] = True
                    else:
                        context['raise'] = 'fields empty'
                        context['status'] = False
                if 'copyItem' in request.POST:
                    icopy = BudgetItems.objects.get(
                        budget_id=kwargs['budget'],
                        budgeti_id=request.POST['budgeti'])
                    item = (BudgetItems.objects.filter(
                        budget_id=kwargs['budget']
                    ).count() + 1)
                    add = BudgetItems(
                        budget_id=kwargs['budget'],
                        item=item,
                        budgeti_id='%s%s' % (
                            kwargs['budget'], '{:0>3d}'.format(item)),
                        name='%s %s' % (icopy.name, 'Copia'),
                        base=icopy.base,
                        offer=icopy.offer,
                        tag=icopy.tag
                    )
                    add.save()
                    # copy details budget
                    context['status'] = True
                if 'delItem' in request.POST:
                    # delete details item
                    # delete bedside item
                    item = BudgetItems.objects.get(
                        budget_id=kwargs['budget'],
                        budgeti_id=request.POST['budgeti'])
                    item.delete()
                    context['status'] = True
                if 'delItemsAll' in request.POST:
                    # delete all details items
                    # delete all items
                    BudgetItems.objects.filter(
                        budget_id=kwargs['budget']).delete()
                    context['status'] = True
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)


class BudgetItemDetails(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            context = dict()
            if request.is_ajax():
                try:
                    if 'item' in request.GET:
                        context['lit'] = simplejson.loads(
                            serializers.serialize(
                                'json', [BudgetItems.objects.get(
                                    budget_id=kwargs['budget'],
                                    budgeti_id=kwargs['item'])]))
                        context['status'] = True
                    if 'listDetails' in request.GET:
                        context['lanalysis'] = simplejson.loads(
                            serializers.serialize(
                                'json',
                                BudgetDetails.objects.filter(
                                    budget_id=kwargs['budget'],
                                    budgeti_id=kwargs['item']),
                                indent=4,
                                relations={
                                    'analysis': {
                                        'extras': ('total',)
                                    }
                                }))
                        context['status'] = True
                    if 'searchAnalysis' in request.GET:
                        analysis = None
                        if request.GET['searchBy'] == 'APDesc':
                            print request.GET
                            analysis = Analysis.objects.filter(
                                name__icontains=request.GET['searchVal'])
                        if request.GET['searchBy'] == 'APCode':
                            analysis = Analysis.objects.filter(
                                analysis_id__istartswith=request.GET[
                                    'searchVal'])
                        if analysis:
                            context['analysis'] = [
                                {
                                    'analysis': x.analysis_id,
                                    'name': x.name,
                                    'performance': x.performance,
                                    'unit': x.unit.uninom,
                                    'amount': x.total
                                }
                                for x in analysis
                            ]
                            context['status'] = True
                        else:
                            context['status'] = False
                except ObjectDoesNotExist as e:
                    context['raise'] = str(e)
                    context['status'] = False
                return self.render_to_json_response(context)
            context = kwargs
            print context
            return render(request, 'budget/budgetdetails.html', context)
        except TemplateDoesNotExist as e:
            raise Http404(e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'addAnalysis' in request.POST:
                    # BudgetDetails(
                    #     budget_id=kwargs['budget'],
                    #     budgeti_id=kwargs['item'],
                    #     analysis_id=request.POST['analysis'],
                    #     quantity=request.POST['quantity']
                    # ).save()
                    # create copy Analysis
                    bd = Budget.objects.get(
                        budget_id=kwargs['budget'],
                        version=kwargs['version'])
                    ap = Analysis.objects.get(
                        analysis_id=request.POST['analysis'])
                    # copy bedside analysis price
                    adc = AnalysisDetails(
                        adetails_id='%s%s' % (
                            kwargs['item'],
                            request.POST['analysis']),
                        analysis_id=request.POST['analysis'],
                        name=ap.name,
                        unit=ap.unit,
                        performance=ap.performance,
                        flag=True)
                    adc.save()
                    # save ap materials
                    # for m in APMaterials.objects.filter(
                    #         request.POST['analysis']):
                    # DAPMaterials(
                    #     adetails_id=adetails_id='%s%s' % (
                    #                     kwargs['item'],
                    #                     request.POST['analysis']),
                    #     materials_id=m.materials_id,
                    #     quantity=m.quantity
                    #     price=m.price
                    #     flag=True
                    # ).save()
                    print bd
                    # copy details analysis materiales, man power and tools
                    context['status'] = True
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
