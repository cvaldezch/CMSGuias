#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.views.generic import TemplateView


from .models import *
from CMSGuias.apps.home.models import Employee
from .forms import EmployeeForm


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


class HomeView(TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            return render(request, 'agenda/index.html', context)
        except TemplateDoesNotExist as e:
            raise Http404(e)


class EmployeeView(JSONResponseMixin, TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'list' in request.GET:
                    context['employee'] = simplejson.loads(
                        serializers.serialize(
                            'json', Employee.objects.filter(flag=True),
                            relations=('charge',)))
                    context['status'] = True
            except ObjectDoesNotExist as e:
                context['raise'] = str(e)
                context['status'] = False
            return self.render_to_json_response(context)
        try:
            return render(request, 'agenda/employee.html')
        except TemplateDoesNotExist, e:
            raise Http404(e)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            if 'save' in request.POST:
                employee = Employee.objects.get(
                            empdni_id=request.POST['empdni_id'])
                if employee:
                    form = EmployeeForm(request.POST, instance=employee)
                else:
                    form = EmployeeForm()
                print form
                if form.is_valid():
                    form.save()
                    context['status'] = True
                else:
                    context['status'] = False
                    context['raise'] = 'fields error.'
        except ObjectDoesNotExist as e:
            context['raise'] = str(e)
            context['status'] = False
        return self.render_to_json_response(context)
