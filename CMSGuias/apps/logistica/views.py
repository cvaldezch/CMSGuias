# -*- coding: utf-8 -*-

import json

from django.db.models import Q, Count
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404,get_object_or_404
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.template import RequestContext, TemplateDoesNotExist
from django.views.generic import TemplateView, View, ListView

from .models import Cotizacion
from CMSGuias.apps.almacen.models import Suministro
from CMSGuias.apps.tools import globalVariable

### Class Bases Views generic

# view home logistics
class LogisticsHome(TemplateView):
    template_name = "logistics/home.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LogisticsHome, self).dispatch(request, *args, **kwargs)

# Class view Supply
class SupplyPending(TemplateView):
    template_name = "logistics/supplypending.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = super(SupplyPending, self).get_context_data(**kwargs)
        if request.GET.get("rdo") is not None:
            print 'ingreso'
            try:
                if request.GET.get('rdo') == 'code':
                    try:
                      model = Suministro.objects.get(pk=request.GET.get('id-su'),flag=True, status='PE')
                    except Suministro.DoesNotExist:
                        print request.path
                        messages.warning( request, 'No se ha encontrado Suministro', extra_tags='<a href="%s">Regresat</a>'%request.path)
                        raise Http404
                elif request.GET.get('rdo') == 'date':
                    if request.GET.get('fi-su') != '' and request.GET.get('ff-su') == '':
                        messages.error(request, 'Ha ocurrido un error miestras se realizaba la consulta %s'%(str(request)))
                        model = Suministro.objects.filter(flag=True, status='PE', registrado__startswith=globalVariable.format_str_date(_str=request.GET.get('fi-su')))
                    elif request.GET.get('fi-su') != '' and request.GET.get('ff-su') != '':
                        model = Suministro.objects.filter(flag=True, status='PE', registrado__range=(globalVariable.format_str_date(request.GET.get('fi-su')),globalVariable.format_str_date(request.GET.get('ff-su'))))
            except ObjectDoesNotExist:
                messages.error(request, 'Ha ocurrido un error miestras se realizaba la consulta %s'%(str(request)))
                raise Http404('Method Error')
        else:
            messages.error(request, 'Ha ocurrido un error')
            model = get_list_or_404(Suministro, flag=True, status='PE')

        paginator = Paginator(model, 20)
        page = request.GET.get('page')
        try:
            supply = paginator.page(page)
        except PageNotAnInteger:
            supply = paginator.page(1)
        except EmptyPage:
            supply = paginator.page(paginator.num_pages)
        context['supply'] = supply
        context['status'] = globalVariable.status
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))