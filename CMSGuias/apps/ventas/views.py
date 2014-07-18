#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from django.db.models import Q, Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404,get_object_or_404
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.template import RequestContext, TemplateDoesNotExist
from django.views.generic import ListView, TemplateView, View

from .models import *
from .forms import *
from CMSGuias.apps.home.models import *
from CMSGuias.apps.tools import *


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
class ProjectsList(TemplateView):
    template_name = "sales/projects.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = super(ProjectsList, self).get_context_data(**kwargs)
        try:
            context['list'] = Proyecto.objects.filter(flag=True)
            context['country'] = Pais.objects.filter(flag=True)
            context['customers'] = Cliente.objects.filter(flag=True)
            return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        except TemplateDoesNotExist, e:
            messages.error(request, "Template Does Not Exist %s"%e)
            raise Http404("Template Does Not Exist %s"%e)
