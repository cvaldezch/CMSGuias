#-*- Encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.contrib import messages
#from attendance.apps.almacen import models
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required(login_url='/SignUp/')
def view_pedido(request):
	try:
		if request.method == 'GET':
			return render_to_response('almacen/pedido.html',context_instance=RequestContext(request))
	except Exception, e:
		raise e
	
