# -*- coding: utf-8 -*-
# Generate Reports PDF's

import os
from django.conf import settings
import ho.pisa as pisa
import cStringIO as StringIO
import cgi

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from django.template import RequestContext, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from CMSGuias.apps.almacen import models
from CMSGuias.apps.tools import globalVariable, search, number_to_char
from CMSGuias.apps.logistica.models import Cotizacion, CotCliente, DetCotizacion, Compra, DetCompra, ServiceOrder, DetailsServiceOrder
from CMSGuias.apps.ventas.models import Proyecto
from CMSGuias.apps.home.models import Configuracion
from CMSGuias.apps.operations.models import PreOrders, DetailsPreOrders


def fetch_resources(uri, rel):
    path = os.path.join(
        settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL,'')
    )
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
    context = dict()
    try:
        if request.method == 'GET':
            order = get_object_or_404(models.Pedido,pk=pid,status=sts)
            lista = models.Detpedido.objects.filter(pedido_id=pid).order_by('materiales__matnom')
            nipples = models.Niple.objects.filter(pedido_id__exact=pid).order_by('materiales')
            context['order'] = order
            lcount = float(lista.count())
            if lcount > 30:
                sheet = int(float('%.0f'%(lcount)) / 30)
                if float(float('%.2f'%(float(lcount)) / 30)) > sheet:
                    sheet += 1
            else:
                sheet = 1
            counter = 0
            section = list()
            for c in range(sheet):
                dataset = lista[counter:counter+30]
                tmp = list()
                for x in dataset:
                    tmp.append(
                        {
                            'item': counter + 1,
                            'materials': x.materiales_id,
                            'name': '%s - %s'%(x.materiales.matnom, x.materiales.matmed),
                            'unit': x.materiales.unidad.uninom,
                            'brand': x.brand.brand,
                            'model': x.model.model,
                            'quantity': x.cantidad
                        }
                    )
                    counter += 1
                section.append(tmp)
            context['lista'] = section
            context['nipples'] = nipples
            context['tipo'] = globalVariable.tipo_nipples
            html = render_to_string('report/rptordersstore.html',context,context_instance=RequestContext(request))
            return generate_pdf(html)
    except TemplateDoesNotExist, e:
        raise Http404

# report guide referral with format
def rpt_guide_referral_format(request, gid, pg):
    try:
        if request.method == 'GET':
            guide = get_object_or_404(models.GuiaRemision, pk=gid, flag=True)
            det = models.DetGuiaRemision.objects.filter(guia_id__exact=gid, flag=True)
            nipples = models.NipleGuiaRemision.objects.filter(guia_id__exact= gid, flag=True)
            tipo = globalVariable.tipo_nipples #{ "A":"Roscado", "B": "Ranurado","C":"Roscado - Ranurado" }
            ctx = { 'pagesize': 'LEGAL', 'guide': guide, 'det': det, 'nipples': nipples, "tipo": tipo }
            page = 'rptguidereferral' if pg == 'format' else 'rptguidereferralwithout'
            html = render_to_string("report/"+page+".html",ctx,context_instance=RequestContext(request))
            return generate_pdf(html)
    except TemplateDoesNotExist, e:
        raise Http404

# Report Supply
class RptSupply(TemplateView):
    template_name = 'report/rptordersupply.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            context = super(RptSupply, self).get_context_data(**kwargs)
            bedside = get_object_or_404(models.Suministro, pk=kwargs['sid'], flag=True)
            queryset = models.DetSuministro.objects.filter(suministro_id__exact=kwargs['sid'], flag=True)
            queryset = queryset.values(
                'materiales_id',
                'materiales__matnom',
                'materiales__matmed',
                'materiales__unidad__uninom',
                'brand__brand'
            )
            queryset = queryset.annotate(cantidad=Sum('cantshop')).order_by('materiales__matnom')
            context['bedside'] = bedside
            context['details'] = queryset
            if queryset.count() > 30:
                context['sheets'] = int('%.0f'%(float(queryset.count())/30))
            else:
                context['sheets'] = 1
            section = list()
            # print queryset.count()
            # print context['sheets']
            counter = 0
            for g in range(context['sheets']):
                # print g, 'g counter'
                dataset = queryset[counter:counter + 30]
                tm = list()
                for x in dataset:
                    tm.append(
                        {
                            'item': counter + 1,
                            'materials': x['materiales_id'],
                            'name': '%s - %s'%(x['materiales__matnom'], x['materiales__matmed']),
                            'unit': x['materiales__unidad__uninom'],
                            'brand': x['brand__brand'],
                            'quantity': x['cantidad']
                        }
                    )
                    counter += 1

                section.append(tm)
                # section.append(
                #     [
                #         {
                #             'item': g,
                #             'materials': x['materiales_id'],
                #             'name': '%s - %s'%(x['materiales__matnom'], x['materiales__matmed']),
                #             'unit': x['materiales__unidad__uninom'],
                #             'brand': x['brand__brand'],
                #             'quantity': x['cantidad']
                #         }
                #         for x in dataset
                #     ]
                # )
            # print section
            # print len(section)
            context['section'] = section
            context['project'] = Proyecto.objects.filter(proyecto_id__in=bedside.orders.split(','))
            context['status'] = globalVariable.status
            html = render_to_string(self.template_name, context, context_instance=RequestContext(request))
            return generate_pdf(html)
        except TemplateDoesNotExist, e:
            raise Http404(e)

# Report Quote
class RptQuote(TemplateView):
    template_name = "report/rptquote.html"

    def get(self, request, *args, **kwargs):
        context = super(RptQuote, self).get_context_data(**kwargs)
        context['bedside'] = get_object_or_404(Cotizacion, pk=kwargs['qid'])
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
            lista = DetCompra.objects.filter(compra_id=kwargs['pk'])
            igv = 0
            subt = 0
            total = 0
            # conf = Configuracion.objects.get(periodo=globalVariable.get_year)
            search.getIGVCurrent(context['bedside'].registrado.strftime('%Y'))
            tdiscount = 0
            # print conf.igv
            lcount = float(lista.count())
            sheet = 0
            if lcount > 20:
                sheet = int(float('%.0f' % (lcount)) / 20)
                if float(float('%.2f' % (lcount)) / 20) > sheet:
                    sheet += 1
            else:
                sheet = 1
            counter = 0
            section = list()
            for c in range(sheet):
                dataset = lista[counter:counter+20]
                tmp = list()
                for x in dataset:
                    disc = ((x.precio * float(x.discount)) / 100)
                    #tdiscount += (disc * x.cantstatic)
                    precio = x.precio - disc
                    amount = (x.cantstatic * precio)
                    subt += amount
                    tmp.append(
                            {
                                'item': counter + 1,
                                'materials_id': x.materiales_id,
                                'matname': x.materiales.matnom,
                                'measure': x.materiales.matmed,
                                'unit': x.materiales.unidad_id,
                                'brand': x.brand.brand,
                                'model': x.model.model,
                                'quantity': x.cantstatic,
                                'price': x.precio,
                                'discount': float(x.discount),
                                'amount': amount
                            }
                    )
                    counter += 1
                section.append(tmp)
            context['details'] = section
            igv = search.getIGVCurrent(context['bedside'].registrado.strftime('%Y'))
            context['subtotal'] = subt
            # print context['bedside'].discount, 'DISCOUNT'
            discount = ((subt * context['bedside'].discount) / 100)
            # print discount
            ns = (subt - discount)
            context['discount'] = discount
            context['igvval'] = ((igv * ns) / 100)
            context['igv'] = igv
            total = (context['igvval'] + ns)
            context['total'] = total
            context['literal'] = number_to_char.numero_a_letras(total)
            context['status'] = globalVariable.status
            html = render_to_string(self.template_name, context, context_instance=RequestContext(request))
            return generate_pdf(html)
        except TemplateDoesNotExist, e:
            raise Http404

# Report Note Inrgess
class RptNoteIngress(TemplateView):
    template_name = "report/rptnoteingress.html"

    @method_decorator(login_required)
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

# Report Service Orders
class RptServiceOrder(TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            context['bedside'] = get_object_or_404(ServiceOrder, Q(serviceorder_id=kwargs['pk']), Q(status='PE'), Q(flag=True))
            context['details'] = DetailsServiceOrder.objects.filter(serviceorder_id=kwargs['pk'])
            details = context['details']
            amount = 0
            for x in details:
                amount += float(x.amount)
            context['amount'] = '%.2f'%amount
            amount = (amount - (amount * (context['bedside'].dsct / 100)))
            context['dsct'] = '%.3f'%(amount * (context['bedside'].dsct / 100))
            context['igv'] = search.getIGVCurrent(context['bedside'].register.strftime('%Y'))
            context['qigv'] = '%.3f'%(amount * (float(context['igv']) / 100))
            context['total'] = '%.2f'%(amount + float(context['qigv']))
            context['literal'] = number_to_char.numero_a_letras(float(context['total']))
            context['status'] = globalVariable.status
            context['pagesize'] = 'A4'
            html = render_to_string('report/rptserviceorders.html', context, context_instance=RequestContext(request))
            return generate_pdf(html)
        except TemplateDoesNotExist, e:
            raise Http404(e)

class RptPreOrders(TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            context = dict()
            context['bedside'] = PreOrders.objects.get(preorder_id=kwargs['porder'])
            lista = DetailsPreOrders.objects.filter(preorder_id=kwargs['porder'])
            sheet = 0
            counter = lista.count()
            if counter >= 30:
                divisible = (counter/30)
                if divisible > round(divisible, 1):
                    sheet = round(divisible, 0) + 1
                else:
                    sheet = round(divisible)
            else:
                sheet = 1
            # print sheet
            count = 0
            context['details'] = list()
            for s in range(sheet):
                dataset = lista[count:count+30]
                tmp = list()
                for x in dataset:
                    # disc = ((x.precio * float(x.discount)) / 100)
                    #tdiscount += (disc * x.cantstatic)
                    #precio = x.precio - disc
                    #amount = (x.cantstatic * precio)
                    #subt += amount
                    tmp.append(
                            {
                                'item': count,
                                'materials_id': x.materials_id,
                                'name': x.materials.matnom,
                                'meter': x.materials.matmed,
                                'unit': x.materials.unidad.uninom,
                                'brand': x.brand.brand,
                                'model': x.model.model,
                                'quantity': x.quantity,
                            }
                    )
                    count += 1
                context['details'].append(tmp)
            context['status'] = globalVariable.status
            context['pagesize'] = 'A4'
            html = render_to_string('report/rptpreorders.html', context, context_instance=RequestContext(request))
            return generate_pdf(html)
        except TemplateDoesNotExist, e:
            raise Http404(e)