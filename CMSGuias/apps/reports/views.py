# -*- coding: utf-8 -*-
#Generate Reports PDF's

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
from django.db.models import Count, Sum
from django.views.generic import TemplateView

from CMSGuias.apps.almacen import models
from CMSGuias.apps.tools import globalVariable
from CMSGuias.apps.logistica.models import Cotizacion, CotCliente, DetCotizacion, Compra, DetCompra
from CMSGuias.apps.home.models import Configuracion

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
            lista = get_list_or_404(models.Detpedido.objects.order_by('materiales__matnom'),pedido_id__exact=pid)
            nipples = models.Niple.objects.filter(pedido_id__exact=pid).order_by('materiales')
            ctx = { 'pagesize':'A4','order': order, 'lista': lista, 'nipples': nipples,'tipo': globalVariable.tipo_nipples }
            html = render_to_string('report/rptordersstore.html',ctx,context_instance=RequestContext(request))
            return generate_pdf(html)
    except TemplateDoesNotExist, e:
        raise Http404
# report guide referral with format
def rpt_guide_referral_format(request,gid,pg):
    try:
        if request.method == 'GET':
            guide = get_object_or_404(models.GuiaRemision, pk=gid, flag=True)
            det = get_list_or_404(models.DetGuiaRemision, guia_id__exact=gid, flag=True)
            nipples = get_list_or_404(models.NipleGuiaRemision, guia_id__exact= gid, flag=True)
            tipo = globalVariable.tipo_nipples #{ "A":"Roscado", "B": "Ranurado","C":"Roscado - Ranurado" }
            ctx = { 'guide': guide, 'det': det, 'nipples': nipples, "tipo": tipo }
            page = 'rptguidereferral' if pg == 'format' else 'rptguidereferralwithout'
            html = render_to_string("report/"+page+".html",ctx,context_instance=RequestContext(request))
            return generate_pdf(html)
    except TemplateDoesNotExist, e:
        raise Http404

# Report Supply
class RptSupply(TemplateView):
    template_name = 'report/rptordersupply.html'

    def get(self, request, *args, **kwargs):
        try:
            context = super(RptSupply, self).get_context_data(**kwargs)
            bedside = get_object_or_404(models.Suministro, pk=kwargs['sid'], flag=True)
            queryset = models.DetSuministro.objects.filter(suministro_id__exact=kwargs['sid'], flag=True)
            queryset = queryset.values('materiales_id','materiales__matnom','materiales__matmed','materiales__unidad_id')
            queryset = queryset.annotate(cantidad=Sum('cantshop')).order_by('materiales__matnom')
            context['bedside'] = bedside
            context['details'] = queryset
            context['status'] = globalVariable.status
            html = render_to_string(self.template_name, context, context_instance=RequestContext(request))
            return generate_pdf(html)
        except TemplateDoesNotExist:
            raise Http404

# Report Quote
class RptQuote(TemplateView):
    template_name = "report/rptquote.html"

    def get(self, request, *args, **kwargs):
        context = super(RptQuote, self).get_context_data(**kwargs)
        context['bedside'] = get_object_or_404(Cotizacion, pk=kwargs['qid'], flag=True)
        context['customers'] = CotCliente.objects.filter(cotizacion_id=kwargs['qid'], proveedor_id=kwargs['pid'])
        context['details'] = DetCotizacion.objects.filter(cotizacion_id=kwargs['qid'],proveedor_id=kwargs['pid'])
        context['status'] = globalVariable.status
        html = render_to_string(self.template_name, context, context_instance=RequestContext(request))
        return generate_pdf(html)

# Report Order Purchase
class RptPurchase(TemplateView):
    template_name = "report/rptpurchase.html"

    def get(self, request, *args, **kwargs):
        try:
            context = dict()
            context['bedside'] = Compra.objects.get(pk=kwargs['pk'], flag=True)
            tmp = DetCompra.objects.filter(compra_id=kwargs['pk'])
            igv = 0
            subt = 0
            total = 0
            conf = Configuracion.objects.get(periodo=globalVariable.get_year)
            tdiscount = 0
            # print conf.igv
            context['details'] = list()
            for x in tmp:
                disc = ((x.precio * x.discount) / 100)
                tdiscount += (disc * x.cantidad)
                precio = x.precio - disc
                amount = (x.cantidad * precio)
                subt += amount
                context['details'].append({'materials_id':x.materiales_id, 'matname':x.materiales.matnom, 'measure': x.materiales.matmed, 'unit':x.materiales.unidad_id, 'quantity':x.cantidad, 'price':x.precio, 'discount':x.discount, 'amount':amount})
            context['discount'] = tdiscount
            context['igvval'] = ((conf.igv * subt) / 100)
            context['igv'] = conf.igv
            context['subtotal'] = subt
            context['total'] = (context['igv'] + subt)
            context['status'] = globalVariable.status
            html = render_to_string(self.template_name, context, context_instance=RequestContext(request))
            return generate_pdf(html)
        except TemplateDoesNotExist, e:
            raise Http404

# Report Note Inrgess
class RptNoteIngress(TemplateView):
    template_name = "report/rptnoteingress.html"

    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            context['bedside'] = models.NoteIngress.objects.get(ingress_id=kwargs['pk'])
            context['details'] = models.DetIngress.objects.filter(ingress_id=kwargs['pk']).order_by('materials__matnom')
            context['status'] = globalVariable.status
            html = render_to_string(self.template_name, context, context_instance=RequestContext(request))
            return generate_pdf(html)
        except TemplateDoesNotExist, e:
            raise Http404