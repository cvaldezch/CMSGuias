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
from CMSGuias.apps.operations.models import MetProject, Nipple
from CMSGuias.apps.almacen.models import Inventario, tmpniple, Pedido, Detpedido, Niple
from .models import *
from .forms import *
from CMSGuias.apps.almacen.forms import addOrdersForm
from CMSGuias.apps.operations.forms import NippleForm
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

# View home Operations
class OperationsHome(TemplateView):
    template_name = "operations/home.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(OperationsHome, self).dispatch(request, *args, **kwargs)