#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# standard library
import json

# Django library
from django.db.models import Sum
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.template import TemplateDoesNotExist
from django.views.generic import View

# local Django
from .models import Proyecto, CloseProject
from ..tools.globalVariable import date_now, get_pin
from ..tools.uploadFiles import descompressRAR, get_extension


class JSONResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            mimetype='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        return json.dumps(context,
                                encoding='utf-8',
                                cls=DjangoJSONEncoder)

class ClosedProjectView(JSONResponseMixin, View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            if request.is_ajax():
                try:
                    if 'load' in request.GET:
                        kwargs['closed'] = json.loads(
                            serializers.serialize(
                                'json',
                                CloseProject.objects.filter(
                                        project_id=kwargs['pro'])))
                        kwargs['status'] = True
                    if 'gcomplete' in request.GET:
                        kwargs['complete'] = {
                            'storage': False,
                            'operations': False,
                            'quality': False,
                            'accounting': False,
                            'sales': False}
                        cl = CloseProject.objects.get(project_id=kwargs['pro'])
                        if cl.storageclose != None and cl.storageclose != False:
                            kwargs['complete']['storage'] = True
                        if cl.letterdelivery != None and cl.letterdelivery != '':
                            kwargs['complete']['operations'] = True
                        if cl.documents != None and cl.documents != '':
                            kwargs['complete']['quality'] = True
                        if cl.accounting != None and cl.accounting != False:
                            kwargs['complete']['accounting'] = True
                        if cl.status != None and cl.status != 'PE':
                            kwargs['complete']['sales'] = True
                        kwargs['status'] = True
                except (ObjectDoesNotExist or Exception) as e:
                    kwargs['status'] = False
                    kwargs['raise'] = str(e)
                return self.render_to_json_response(kwargs)
            kwargs['pr'] = Proyecto.objects.get(proyecto_id=kwargs['pro'], flag=True, status='AC')
            return render(request, 'sales/closedproject.html', kwargs)
        except TemplateDoesNotExist as ex:
            raise Http404(ex)
        return HttpResponse('GET request!')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                if 'storage' in request.POST:
                    try:
                        cl = CloseProject.objects.get(project_id=kwargs['pro'])
                    except (CloseProject.DoesNotExist) as ex:
                        cl = CloseProject()
                        cl.project_id=kwargs['pro']
                    cl.storageclose = True
                    cl.datestorage = date_now('datetime')
                    cl.performedstorage_id = request.user.get_profile().empdni_id
                    cl.save()
                    kwargs['status'] = True
                if 'operations' in request.POST:
                    try:
                        cl = CloseProject.objects.get(project_id=kwargs['pro'])
                    except (CloseProject.DoesNotExist or Exception) as ex:
                        cl = CloseProject()
                        cl.project_id=kwargs['pro']
                    cl.letterdelivery = request.FILES['letter']
                    cl.dateletter = date_now('datetime')
                    cl.performedoperations_id = request.user.get_profile().empdni_id
                    cl.save()
                    kwargs['status'] = True
                if 'quality' in request.POST:
                    try:
                        cl = CloseProject.objects.get(project_id=kwargs['pro'])
                    except (CloseProject.DoesNotExist or Exception) as ex:
                        cl = CloseProject()
                        cl.project_id=kwargs['pro']
                    cl.documents = request.FILES['documents']
                    cl.docregister = date_now('datetime')
                    cl.performeddocument_id=request.user.get_profile().empdni_id
                    cl.save()
                    if get_extension(cl.documents.name) == '.rar':
                        descompressRAR(cl.documents)
                    kwargs['status'] = True
                if 'accounting' in request.POST:
                    try:
                        cl = CloseProject.objects.get(project_id=kwargs['pro'])
                    except (CloseProject.DoesNotExist or Exception) as ex:
                        cl = CloseProject()
                        cl.project_id = kwargs['pro']
                    if 'tinvoice' in request.POST:
                        if request.POST['tinvoice'] > -1:
                            cl.tinvoice = request.POST['tinvoice']
                    if 'tiva' in request.POST:
                        if request.POST['tiva'] > -1:
                            cl.tiva = request.POST['tiva']
                    if 'otherin' in request.POST:
                        if request.POST['otherin'] > -1:
                            cl.otherin = request.POST['otherin']
                    if 'otherout' in request.POST:
                        if request.POST['otherout'] > -1:
                            cl.otherout = request.POST['otherout']
                    if 'retention' in request.POST:
                        if request.POST['retention'] > -1:
                            cl.retention = request.POST['retention']
                    if 'fileaccounting' in request.FILES:
                        cl.fileaccounting = request.FILES['fileaccounting']
                    cl.performedaccounting_id = request.user.get_profile().empdni_id
                    cl.save()
                    if get_extension(cl.fileaccounting) == '.rar':
                        descompressRAR(cl.fileaccounting)
                    kwargs['status'] = True
                if 'quitaccounting' in request.POST:
                    cl = CloseProject.objects.get(project_id=kwargs['pro'])
                    cl.accounting = True
                    cl.save()
                    kwargs['status'] = True
                if 'sales' in request.POST:
                    cl = CloseProject.objects.get(project_id=kwargs['pro'])
                    if 'genpin' in request.POST:
                        cl.closeconfirm = get_pin()
                        cl.save()
                        kwargs['pin'] =  cl.closeconfirm
                        kwargs['company'] = request.session['company']['name']
                        kwargs['name'] = cl.project.nompro
                        kwargs['mail'] = request.user.get_profile().empdni.email
                        kwargs['status'] = True
                    if 'closed' in request.POST:
                        if request.POST['confirm'] == cl.closeconfirm:
                            cl.dateclose = date_now('datetime')
                            cl.performedclose_id = request.user.get_profile().empdni_id
                            cl.status = 'CO'
                            cl.save()
                            pr = Proyecto.objects.get(proyecto_id=kwargs['pro'])
                            pr.status = 'CL'
                            pr.flag = False
                            pr.save()
                            kwargs['status'] = True
            except (ObjectDoesNotExist or Exception) as e:
                kwargs['raise'] = str(e)
                kwargs['status'] = False
            return self.render_to_json_response(kwargs)
