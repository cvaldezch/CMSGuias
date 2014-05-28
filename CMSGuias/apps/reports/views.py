"""
		generate pdf reports
"""
import os
from django.conf import settings
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib import messages
from django.template import RequestContext, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from CMSGuias.apps.almacen import models
from django.db.models import Count

def fetch_resources(uri, rel):
	path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
	return path

def generate_pdf(html):
	# functions for generate the file PDF and return HttpResponse
	#pisa.showLogging(debug=True)
	result = StringIO.StringIO()
	#links = lambda uri, rel: os.path.join(settings.MEDIA_ROOT,uri.replace(settings.MEDIA_URL, ''))
	#print links
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
	if not pdf.err:
		return HttpResponse(result.getvalue(), mimetype="application/pdf")
	return HttpResponse("error al generar el PDF: %s"%cgi.escape(html))
"""
   block generate pdf test
"""
def view_test_pdf(request):
	# view of poseable result pdf
	html = render_to_string('report/test.html',{'pagesize':'A4'},context_instance=RequestContext(request))
	return generate_pdf(html)
"""
		end block
"""
### Reports 
def rpt_orders_details(request,pid,sts):
	try:
		if request.method == 'GET':
			order = get_object_or_404(models.Pedido,pk=pid,status=sts)
			lista = get_list_or_404(models.Detpedido,pedido_id__exact=pid)
			nipples = models.Niple.objects.filter(pedido_id__exact=pid)
			ctx = { 'pagesize':'A4','order': order, 'lista': lista, 'nipples': nipples }
			html = render_to_string('report/rptordersstore.html',ctx,context_instance=RequestContext(request))
			return generate_pdf(html)
	except TemplateDoesNotExist, e:
		raise Http404

# report guide referral with format
def rpt_guide_referral_format(request,gid,pg):
	try:
		if request.method == 'GET':
			guide= get_object_or_404(models.GuiaRemision, pk=gid, flag=True)
			det= get_list_or_404(models.DetGuiaRemision, guia_id__exact=gid, flag=True)
			nipples= get_list_or_404(models.NipleGuiaRemision, guia_id__exact= gid, flag=True)
			tipo= { "A":"Roscado", "B": "Ranurado","C":"Roscado - Ranurado" }
			ctx= { 'guide': guide, 'det': det, 'nipples': nipples, "tipo": tipo }
			page= 'rptguidereferral' if pg == 'format' else 'rptguidereferralwithout'
			html= render_to_string("report/"+page+".html",ctx,context_instance=RequestContext(request))
			return generate_pdf(html)
	except TemplateDoesNotExist, e:
		raise Http404