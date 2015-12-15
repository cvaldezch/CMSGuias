#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import json

from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
# from django.contrib import messages
# from django.contrib.auth.mod import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.db.models import Q, Sum
from django.shortcuts import render_to_response, render
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.template import RequestContext, TemplateDoesNotExist
from django.views.generic import TemplateView, View
# from django.views.generic.edit import UpdateView, CreateView
from django.core.serializers.json import DjangoJSONEncoder

from CMSGuias.apps.home.models import *
from .models import *
from .forms import *
from CMSGuias.apps.ventas.models import Metradoventa
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
        return simplejson.dumps(context,
                                encoding='utf-8',
                                cls=DjangoJSONEncoder)


# View home Operations
class OperationsHome(TemplateView):
    template_name = 'operations/home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(OperationsHome, self).dispatch(request, *args, **kwargs)


# View list pre orders
class ListPreOrders(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            context = dict()
            context['list'] = PreOrders.objects.filter(
                project_id=kwargs['pro'],
                sector_id=kwargs['sec'],
                status='PE'
            ).order_by('-register')
            context['status'] = globalVariable.status
            return render_to_response(
                'operations/listpreorders.html',
                context,
                context_instance=RequestContext(request))
        except TemplateDoesNotExist, e:
            raise Http404(e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'anullarPreOrders' in request.POST:
                    obj = PreOrders.objects.get(
                        preorder_id=request.POST['pre'])
                    obj.annular = request.POST.get('annular')
                    obj.status = 'AN'
                    obj.save()
                    context['status'] = True
                if 'changeComplete' in request.POST:
                    obj = PreOrders.objects.get(
                        preorder_id=request.POST['pre'])
                    obj.status = 'CO'
                    obj.save()
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
        else:
            context['list'] = PreOrders.objects.filter(
                project_id=kwargs['pro'],
                sector_id=kwargs['sec'],
                status=request.POST.get('status')
            ).order_by('-register')
            context['search'] = request.POST.get('status')
            context['status'] = globalVariable.status
            return render_to_response(
                'operations/listpreorders.html',
                context,
                context_instance=RequestContext(request))


class ProgramingProject(JSONResponseMixin, View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'listg' in request.GET:
                    sg = SGroup.objects.filter(
                            project_id=kwargs['pro'],
                            subproject_id=kwargs[
                                'sub'] if unicode(kwargs[
                                    'sub']) != 'None' and unicode(kwargs[
                                        'sub']) != '' else None,
                            sector_id=kwargs['sec']).order_by('name')
                    context['sg'] = json.loads(serializers.serialize(
                                                                'json', sg))
                    context['status'] = True
                if 'listds' in request.GET:
                    ds = DSector.objects.filter(
                            project_id=kwargs['pro'],
                            sgroup__subproject_id=kwargs[
                                'sub'] if unicode(kwargs[
                                    'sub']) != 'None' and unicode(kwargs[
                                        'sub']) != '' else None,
                            sgroup__sector_id=kwargs['sec']).order_by(
                            'sgroup')
                    context['ds'] = json.loads(serializers.serialize(
                                        'json',
                                        ds,
                                        relations=('sgroup',)))
                    context['status'] = True
                if 'valPrices' in request.GET:
                    # get sgroup
                    sg = [x[0] for x in SGroup.objects.filter(
                            project_id=kwargs['pro'],
                            subproject_id=kwargs[
                                'sub'] if unicode(kwargs[
                                    'sub']) != 'None' and unicode(kwargs[
                                        'sub']) != '' else None,
                            sector_id=kwargs['sec']).values_list('sgroup_id',)]
                    sec = [x[0] for x in DSector.objects.filter(
                            sgroup_id__in=sg).values_list('dsector_id')]
                    without = DSMetrado.objects.filter(
                        Q(dsector_id__in=sec),
                        Q(ppurchase=0) | Q(psales=0) | Q(quantity=0)
                        ).order_by('materials__matnom')
                    if without:
                        context['list'] = json.loads(
                            serializers.serialize(
                                'json',
                                without,
                                relations=('materials',),
                                indent=4))
                        context['status'] = True
                    else:
                        context['status'] = False
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = Falses
            return self.render_to_json_response(context)
        else:
            try:
                context['project'] = Proyecto.objects.get(
                    proyecto_id=kwargs['pro'])
                context['sector'] = Sectore.objects.get(
                    proyecto_id=kwargs['pro'],
                    subproyecto_id=kwargs['sub'] if kwargs[
                        'sub'] is None else None,
                    sector_id=kwargs['sec'])
                return render(
                    request,
                    'operations/programinggroup.html',
                    context)
            except TemplateDoesNotExist, e:
                raise Http404(e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'saveg' in request.POST:
                    try:
                        if 'sgroup_id' in request.POST:
                            sg = SGroup.objects.get(
                                    sgroup_id=request.POST['sgroup_id'])
                            form = SGroupForm(request.POST, instance=sg)
                        else:
                            form = SGroupForm(request.POST)
                    except ObjectDoesNotExist:
                        form = SGroupForm(request.POST)
                    if form.is_valid():
                        if 'sgroup_id' not in request.POST:
                            add = form.save(commit=False)
                            key = genkeys.genSGroup(
                                    kwargs['pro'], kwargs['sec'])
                            add.sgroup_id = key.strip()
                            add.project_id = kwargs['pro']
                            if unicode(kwargs['sub']) != 'None':
                                add.subproject_id = kwargs['sub']
                            add.sector_id = kwargs['sec']
                            add.colour = request.POST['rgba']
                            add.save()
                        else:
                            edit = form.save(commit=False)
                            edit.colour = request.POST['rgba']
                            edit.save()
                        context['status'] = True
                    else:
                        context['status'] = False
                if 'saveds' in request.POST:
                    try:
                        if 'dsector_id' in request.POST:
                            ds = DSector.objects.get(
                                    dsector_id=request.POST['dsector_id'])
                            form = DSectorForm(
                                    request.POST, request.FILES, instance=ds)
                        else:
                            form = DSectorForm(request.POST, request.FILES)
                    except ObjectDoesNotExist as e:
                        form = DSectorForm(request.POST, request.FILES)
                    print form
                    if form.is_valid():
                        if 'dsector_id' not in request.POST:
                            add = form.save(commit=False)
                            key = genkeys.genDSector(
                                    kwargs['pro'],
                                    request.POST['sgroup'])
                            add.dsector_id = key.strip()
                            add.project_id = kwargs['pro']
                            add.save()
                        else:
                            form.save()
                        try:
                            sg = SGroup.objects.get(
                                    sgroup_id=request.POST['sgroup'])
                            if sg.datestart is None:
                                sg.datestart = request.POST['datestart']
                            else:
                                st = globalVariable.format_str_date(
                                        request.POST['datestart'])
                                if st < sg.datestart:
                                    sg.datestart = st
                            if sg.dateend is None:
                                sg.dateend = request.POST['dateend']
                            else:
                                ed = globalVariable.format_str_date(
                                        request.POST['dateend'])
                                if ed > sg.dateend:
                                    sg.dateend = ed
                            sg.save()
                        except SGroup.DoesNotExist, e:
                            context['raise'] = str(e)
                        context['status'] = True
                    else:
                        context['status'] = False
                        context['raise'] = 'Fields empty'
                if 'savePricewithout' in request.POST:
                    sg = [x[0] for x in SGroup.objects.filter(
                            project_id=kwargs['pro'],
                            subproject_id=kwargs[
                                'sub'] if unicode(kwargs[
                                    'sub']) != 'None' and unicode(kwargs[
                                        'sub']) != '' else None,
                            sector_id=kwargs['sec']).values_list('sgroup_id',)]
                    sec = [x[0] for x in DSector.objects.filter(
                            sgroup_id__in=sg).values_list('dsector_id')]
                    dsm = DSMetrado.objects.filter(
                        dsector_id__in=sec,
                        materials_id=request.POST['materials'])
                    if request.POST['field'] == 'purchase':
                        dsm.update(ppurchase=request.POST['value'])
                    if request.POST['field'] == 'sales':
                        dsm.update(psales=request.POST['value'])
                    context['status'] = True
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)


class AreaProjectView(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'dslist' in request.GET:
                    context['list'] = json.loads(serializers.serialize(
                        'json',
                        DSMetrado.objects.filter(
                            dsector_id=kwargs['area']).order_by(
                            'materials__matnom'), relations=(
                            'materials', 'brand', 'model',)))
                    context['status'] = True
                if 'lstnipp' in request.GET:
                    context['nip'] = json.loads(
                        serializers.serialize(
                            'json',
                            Nipple.objects.filter(
                                area_id=kwargs['area'],
                                materiales_id=request.GET['materials']),
                            relations=('materiales')))
                    context['dnip'] = globalVariable.tipo_nipples
                    context['status'] = True
                if 'typeNipple' in request.GET:
                    context['type'] = globalVariable.tipo_nipples
                    context['status'] = True
                if 'modifyList' in request.GET:
                    context['modify'] = json.loads(
                        serializers.serialize(
                            'json',
                            MMetrado.objects.filter(
                                dsector_id=kwargs['area']).order_by(
                                'materials__matnom'),
                            relations=('materials', 'brand', 'model')))
                    context['status'] = True
                if 'samountp' in request.GET:
                    sg = [x[0] for x in SGroup.objects.filter(
                            project_id=kwargs['pro'],
                            sector_id=kwargs['sec']).values_list('sgroup_id',)]
                    sec = [x[0] for x in DSector.objects.filter(
                            sgroup_id__in=sg).values_list('dsector_id')]
                    dsal = DSMetrado.objects.filter(
                            dsector_id__in=sec).aggregate(
                            tpurchase=Sum(
                                'quantity', field='quantity * ppurchase'),
                            tsales=Sum('quantity', field='quantity * psales')
                        )
                    rds = DSMetrado.objects.filter(dsector_id=kwargs[
                        'area']).aggregate(tpurchase=Sum(
                            'quantity',
                            field='quantity * ppurchase'),
                            tsales=Sum('quantity', field='quantity * psales'))
                    context['msector'] = dsal
                    context['maarea'] = rds
                    mm = MMetrado.objects.filter(
                        dsector_id=kwargs['area']).order_by(
                        'materials__matnom').aggregate(
                        apurchase=Sum(
                            'quantity', field='quantity * ppurchase'),
                        asale=Sum(
                            'quantity', field='quantity * psales'))
                    context['mmodidy'] = mm
                    context['status'] = True
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
        else:
            try:
                context['dsector'] = DSector.objects.get(
                                        dsector_id=kwargs['area'])
                context['modify'] = MMetrado.objects.filter(
                                        dsector_id=kwargs['area']).order_by(
                                            '-register')[:5]
                return render(request, 'operations/dsector.html', context)
            except TemplateDoesNotExist as e:
                raise Http404(e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'savepmat' in request.POST:
                    try:
                        if 'editmat' in request.POST:
                            dsm = DSMetrado.objects.get(
                                dsector_id=kwargs['area'],
                                materials_id=request.POST['code'],
                                brand_id=request.POST['obrand'],
                                model_id=request.POST['omodel'])
                            dsm.brand_id = request.POST['brand']
                            dsm.model_id = request.POST['model']
                            dsm.quantity = float(request.POST['quantity'])
                            dsm.qorder = float(request.POST['quantity'])
                        else:
                            dsm = DSMetrado.objects.get(
                                dsector_id=kwargs['area'],
                                materials_id=request.POST['code'],
                                brand_id=request.POST['brand'],
                                model_id=request.POST['model'])
                            dsm.quantity = (
                                dsm.quantity + float(request.POST['quantity']))
                            dsm.qorder = (
                                dsm.qorder + float(request.POST['quantity']))
                        dsm.ppurchase = request.POST['ppurchase']
                        dsm.psales = request.POST['psales']
                    except DSMetrado.DoesNotExist as e:
                        context['raise'] = str(e)
                        dsm = DSMetrado()
                        dsm.dsector_id = kwargs['area']
                        dsm.materials_id = request.POST['code']
                        dsm.brand_id = request.POST['brand']
                        dsm.model_id = request.POST['model']
                        dsm.quantity = request.POST['quantity']
                        dsm.qorder = request.POST['quantity']
                        dsm.qguide = 0
                        dsm.ppurchase = request.POST['ppurchase']
                        dsm.psales = request.POST['psales']
                    dsm.save()
                    context['status'] = True
                if 'delmat' in request.POST:
                    try:
                        DSMetrado.objects.get(
                            dsector_id=kwargs['area'],
                            materials_id=request.POST['materials'],
                            brand_id=request.POST['brand'],
                            model_id=request.POST['model']).delete()
                        context['status'] = True
                    except DSMetrado.DoesNotExist, e:
                        context['raise'] = str(e)
                if 'copysector' in request.POST:
                    sec = MetProject.objects.filter(
                        proyecto_id=request.POST['project'],
                        sector_id=request.POST['sector'])
                    if not sec:
                        sec = Metradoventa.objects.filter(
                            proyecto_id=request.POST['project'],
                            sector_id=request.POST['sector'])
                    if sec:
                        for x in sec:
                            try:
                                ds = DSMetrado.objects.get(
                                        dsector_id=kwargs['area'],
                                        materials_id=x.materiales_id)
                            except DSMetrado.DoesNotExist:
                                ds = DSMetrado()
                            ds.dsector_id = kwargs['area']
                            ds.materials_id = x.materiales_id
                            ds.brand_id = x.brand_id
                            ds.model_id = x.model_id
                            ds.quantity = x.cantidad
                            ds.qorder = x.cantidad
                            ds.qguide = 0
                            ds.ppurchase = x.precio
                            ds.psales = x.sales
                            ds.save()
                        context['status'] = True
                    else:
                        context['status'] = False
                if 'delAreaMA' in request.POST:
                    DSMetrado.objects.filter(
                        dsector_id=kwargs['area']).delete()
                    context['status'] = True
                if 'availableNipple' in request.POST:
                    dsm = DSMetrado.objects.get(
                        dsector_id=kwargs['area'],
                        materials_id=request.POST['materials'],
                        brand_id=request.POST['brand'],
                        model_id=request.POST['model'])
                    if dsm.nipple:
                        dsm.nipple = False
                        dsm.save()
                    else:
                        dsm.nipple = True
                        dsm.save()
                    context['status'] = True
                if 'nipplesav' in request.POST:
                    try:
                        area = DSector.objects.get(
                                dsector_id=kwargs['area'])
                    except DSector.DoesNotExist:
                        area = {'sector_id': ''}
                    # kw = request.POST
                    request.POST._mutable = True
                    request.POST['proyecto'] = kwargs['area'][:7]
                    request.POST['area'] = kwargs['area']
                    request.POST['sector'] = area.sgroup.sector_id
                    request.POST._mutable = False
                    if 'edit' in request.POST:
                        Np = Nipple.objects.get(
                                id=request.POST['id'],
                                area_id=kwargs['area'],
                                materiales_id=request.POST['materiales'])
                        nip = NippleForm(request.POST, instance=Np)
                    else:
                        nip = NippleForm(request.POST)
                    if nip.is_valid():
                        nip.save()
                        context['status'] = True
                    else:
                        context['status'] = False
                if 'delnipp' in request.POST:
                    Nipple.objects.get(
                        id=request.POST['id'],
                        area_id=kwargs['area'],
                        materiales_id=request.POST['materials']).delete()
                    context['status'] = True
                if 'modifyArea' in request.POST:
                    valid = MMetrado.objects.filter(dsector_id=kwargs['area'])
                    if not valid:
                        clipboard = DSMetrado.objects.filter(
                                        dsector_id=kwargs['area'])
                        if clipboard:
                            for x in clipboard:
                                add = MMetrado()
                                add.dsector_id = kwargs['area']
                                add.materials_id = x.materials_id
                                add.brand_id = x.brand_id
                                add.model_id = x.model_id
                                add.quantity = x.quantity
                                add.qorder = x.qorder
                                add.qguide = x.qguide
                                add.ppurchase = x.ppurchase
                                add.psales = x.psales
                                add.comment = x.comment
                                add.tag = x.tag
                                add.nipple = x.nipple
                                add.flag = x.flag
                                add.save()
                            context['status'] = True
                        else:
                            context['status'] = False
                    else:
                        context['status'] = False
                if 'editMM' in request.POST:
                    update = MMetrado.objects.filter(
                        dsector_id=kwargs['area'],
                        materials_id=request.POST['materials'],
                        brand_id=request.POST['brand'],
                        model_id=request.POST['model'])
                    if update:
                        if request.POST['name'] == 'brand':
                            update[0].brand_id = request.POST['value']
                        if request.POST['name'] == 'model':
                            update[0].model_id = request.POST['value']
                        if request.POST['name'] == 'quantity':
                            update[0].quantity = request.POST['value']
                        if request.POST['name'] == 'ppurchase':
                            update[0].ppurchase == request.POST['value']
                        if request.POST['name'] == 'psales':
                            update[0].psales = request.POST['value']
                        update[0].save()
                        context['status'] = True
                    else:
                        context['status'] = False
                        context['raise'] = 'Data not found'
                if 'delMM' in request.POST:
                    MMetrado.objects.get(
                        dsector_id=kwargs['area'],
                        materials_id=request.POST['materials'],
                        brand_id=request.POST['brand'],
                        model_id=request.POST['model']).delete()
                    context['status'] = True
                if 'annModify' in request.POST:
                    MMetrado.objects.filter(dsector_id=kwargs['area']).delete()
                    context['status'] = True
                if 'savemmat' in request.POST:
                    try:
                        mm = MMetrado.objects.get(
                            dsector_id=kwargs['area'],
                            materials_id=request.POST['code'],
                            brand_id=request.POST['brand'],
                            model_id=request.POST['model'])
                        mm.quantity = (
                            mm.quantity + float(request.POST['quantity']))
                        mm.qorder = (
                            mm.qorder + float(request.POST['quantity']))
                        mm.ppurchase = request.POST['ppurchase']
                        mm.psales = request.POST['psales']
                    except MMetrado.DoesNotExist, e:
                        context['raise'] = str(e)
                        mm = MMetrado()
                        mm.dsector_id = kwargs['area']
                        mm.materials_id = request.POST['code']
                        mm.brand_id = request.POST['brand']
                        mm.model_id = request.POST['model']
                        mm.quantity = request.POST['quantity']
                        mm.qorder = request.POST['quantity']
                        mm.qguide = 0
                        mm.ppurchase = request.POST['ppurchase']
                        mm.psales = request.POST['psales']
                    mm.save()
                    context['status'] = True
                if 'approvedModify' in request.POST:
                    try:
                        pass
                    except Exception, e:
                        context['raise'] = str(e)
                        context['status'] = False
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
