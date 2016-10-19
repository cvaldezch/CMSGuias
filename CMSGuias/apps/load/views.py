# -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from CMSGuias.apps.ventas.models import Proyecto, Painting


class PaintingData(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            pr = Proyecto.objects.filter(flag=True)
            for x in pr:
                try:
                    Painting.objects.get(project_id=x.proyecto_id)
                except Painting.DoesNotExist:
                    Painting.objects.create(project_id=x.proyecto_id,
                                            nlayers=1,
                                            nfilmb=4,
                                            nfilmc=4).save()
            kwargs['status'] = True
        except Exception as e:
            kwargs['status'] = False
            kwargs['raise'] = str(e)
        return HttpResponse(json.dumps(kwargs), mimetype='application/json;charset=utf-8')