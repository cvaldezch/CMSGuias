#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib import messages
# from django.contrib.auth.mod import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, render
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.template import RequestContext, TemplateDoesNotExist
from django.views.generic import TemplateView
# from django.views.generic.edit import UpdateView, CreateView

from CMSGuias.apps.home.models import *
# from CMSGuias.apps.operations.models import MetProject, Nipple
# from CMSGuias.apps.almacen.models import
# Inventario, tmpniple, Pedido, Detpedido, Niple
from .models import *
from .forms import *
# from CMSGuias.apps.almacen.forms import addOrdersForm
# from CMSGuias.apps.operations.forms import NippleForm
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
        return simplejson.dumps(context, encoding='utf-8')


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


class ProgramingProject(JSONResponseMixin, TemplateView):

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
                    print form
                    print form.is_valid()
                    if form.is_valid():
                        if 'edit' not in request.POST:
                            add = form.save(commit=False)
                            key = genkeys.genSGroup(
                                    kwargs['pro'], kwargs['sec'])
                            print key, len(key)
                            add.sgroup_id = key.strip()
                            add.project_id = kwargs['pro']
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
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
