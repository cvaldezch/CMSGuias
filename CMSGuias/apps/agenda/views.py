#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
# from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.views.generic import TemplateView


from .models import *
# from CMSGuias.apps.home.models import Employee


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
