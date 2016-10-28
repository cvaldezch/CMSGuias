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

class ClosedProjectView(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            if request.is_ajax():
                try:
                    pass
                except (ObjectDoesNotExist or Exception) as e:
                    kwargs['status'] = False
                    kwargs['raise'] = str(e)
                return self.render_to_json_response(kwargs)
            kwargs['pr'] = Proyecto.objects.get(proyecto_id=kwargs['pro'], flag=True, status='AC')
            return render(request, 'sales/closedproject.html', kwargs)
        except TemplateDoesNotExist as ex:
            raise Http404(ex)
        return HttpResponse('GET request!')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                if 'storage' in request.POST:
                    try:
                        cl = CloseProject.objects.get(project_id=kwargs['pro'])
                        cl.storageclose = True
                        cl.datestorage = datetime.datetime.today()
                        cl.performedstorage_id = request.user.get_profile().empdni_id
                        cl.save()
                    except (CloseProject.DoesNotExist) as ex:
                        CloseProject.objects.create(
                            project_id=kwargs['pro'],
                            storageclose=True,
                            performedstorage_id=request.user.get_profile().empdni_id)
                        kwargs['status'] = True
                if 'operations' in request.POST:
                    try:
                        pass
                    except (CloseProject.DoesNotExist or Exception) as ex:
                        pass
                if 'quality' in request.POST:
                    pass
                if 'accounting' in request.POST:
                    pass
                if 'sales' in request.POST:
                    pass
            except (ObjectDoesNotExist or Exception) as e:
                kwargs['raise'] = str(e)
                kwargs['status'] = False
            return self.render_to_json_response(kwargs)
