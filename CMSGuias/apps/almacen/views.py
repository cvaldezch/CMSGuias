#-*- Encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.contrib import messages
#from attendance.apps.almacen import models
from django.db.models import Count

def view_home(request):
	if request.method == 'GET':
		return render_to_response('almacen/home.html',context_instance=RequestContext(request))
