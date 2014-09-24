 # -*- coding: utf-8 -*-

import json
import hashlib

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
from django.views.generic.edit import CreateView
from xlrd import open_workbook, XL_CELL_EMPTY

from CMSGuias.apps.almacen.models import Suministro
from CMSGuias.apps.home.models import Proveedor, Documentos, FormaPago, Almacene, Moneda, Configuracion, LoginProveedor, Brand, Model
from .models import Compra, Cotizacion, CotCliente, CotKeys, DetCotizacion, DetCompra, tmpcotizacion, tmpcompra
from CMSGuias.apps.tools import genkeys, globalVariable, uploadFiles
from .forms import addTmpCotizacionForm, addTmpCompraForm, CompraForm, ProveedorForm


### Class Bases Views generic

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
            if request.GET.get('rdo') == 'code':
                model = Suministro.objects.filter(pk=request.GET.get('id-su'),flag=True, status='PE')
            elif request.GET.get('rdo') == 'date':
                if request.GET.get('fi-su') != '' and request.GET.get('ff-su') == '':
                    messages.error(request, 'Ha ocurrido un error miestras se realizaba la consulta %s'%(str(request)))
                    model = Suministro.objects.filter(flag=True, status='PE', registrado__startswith=globalVariable.format_str_date(_str=request.GET.get('fi-su')))
                elif request.GET.get('fi-su') != '' and request.GET.get('ff-su') != '':
                    model = Suministro.objects.filter(flag=True, status='PE', registrado__range=(globalVariable.format_str_date(request.GET.get('fi-su')),globalVariable.format_str_date(request.GET.get('ff-su'))))
        else:
            model = Suministro.objects.filter(flag=True, status='PE')

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

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = {}
        if request.is_ajax():
            try:
                obj = Suministro.objects.get(flag=True, status='PE', pk=request.POST.get('id-su'))
                obj.status = 'AP' if request.POST.get('status') == "approve" else 'AN'
                obj.save() # update status supply
                context['status'] = True
            except ObjectDoesNotExist:
                messages.error(request, "Se ha encontrado error al cambiar el status de supply", messages.ERROR);
                raise Http404
                context['status'] = False
            context['type'] = request.POST.get('status')
            context = simplejson.dumps(context)
            return HttpResponse(context, mimetype="application/json", content_type="application/json")

# Class view Convert Supply to quote or Purchase
class SupplytoDocumentIn(TemplateView):
    template_name = "logistics/spdocumentin.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = super(SupplytoDocumentIn, self).get_context_data(**kwargs)
        model = Suministro.objects.filter(flag=True, status='AP')
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
        context['supplier'] = Proveedor.objects.filter(flag=True)
        context['storage'] = Almacene.objects.filter(flag=True)
        context['documents'] = Documentos.objects.filter(flag=True)
        context['payment'] = FormaPago.objects.filter(flag=True)
        context['currency'] = Moneda.objects.filter(flag=True)
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST.get("type") == "finish":
                data = {}
                try:
                    obj =  Suministro.objects.get(pk=request.POST.get('supply'))
                    obj.status = 'CO'
                    obj.flag = False
                    obj.save()
                    data['obj'] = True
                except ObjectDoesNotExist, e:
                    data['status'] = False
                return HttpResponse(simplejson.dumps(data), mimetype='application/json', content_type='application/json')

            response = HttpResponse()
            data = {}
            try:
                # get status type document
                if request.POST.get('type') == "quote":
                    # saved quotation
                    idquote = None
                    if request.POST.get('newid') == "1":
                        # recover data for header quote and save
                        idquote = genkeys.GenerateKeyQuotation()
                        obj = Cotizacion()
                        obj.cotizacion_id = idquote
                        obj.suministro_id = request.POST.get('supply')
                        obj.empdni_id = request.user.get_profile().empdni_id
                        obj.almacen_id = request.POST.get('storage')
                        obj.traslado = globalVariable.format_str_date(request.POST.get('traslado'))
                        obj.obser = request.POST.get('obser')
                        obj.status = 'PE'
                        obj.flag = True
                        obj.save()
                    elif request.POST.get('newid') == "0":
                        idquote = request.POST.get('id')

                    # save quote to client
                    counter = CotKeys.objects.filter(cotizacion_id=idquote, proveedor_id=request.POST.get('supplier')).aggregate(counter=Count('cotizacion'))
                    if counter['counter'] == 0:
                        obj = CotKeys()
                        obj.cotizacion_id = idquote
                        obj.proveedor_id = request.POST.get('supplier')
                        obj.keygen = genkeys.GeneratekeysQuoteClient()
                        obj.status = "PE"
                        obj.flag = True
                        obj.save()

                    # save det quote
                    mats = json.loads(request.POST.get('mats'))
                    for x in range(mats.__len__()):
                        obj = DetCotizacion()
                        obj.cotizacion_id = idquote
                        obj.proveedor_id = request.POST.get('supplier')
                        obj.materiales_id = mats[x]['mid']
                        obj.cantidad = mats[x]['cant']
                        obj.flag = True
                        obj.save()

                    data["id"] = idquote
                    data['status'] = True
                elif request.POST.get('type') == "buy":
                    data['status'] = True
            except ObjectDoesNotExist, e:
                print e
                data['status'] = False
            response.write(simplejson.dumps(data))
            response['content_type'] = "application/json"
            response['mimetype'] = "application/json"
            return response

class ViewListQuotation(TemplateView):
    template_name = "logistics/listquotation.html"

    def get(self, request, *args, **kwargs):
        context = super(ViewListQuotation, self).get_context_data(**kwargs)
        if request.is_ajax():
            if request.GET.get('by') == 'code':
                model = CotKeys.objects.filter(Q(cotizacion_id=request.GET.get('code')), Q(flag=True),~Q(status='CO'), ~Q(status='NC') )
            elif request.GET.get('by') == 'dates':
                if request.GET.get('dates') != '' and request.GET.get('datee') == '':
                    model = CotKeys.objects.filter(Q(cotizacion__registrado__startswith=globalVariable.format_str_date(request.GET.get('dates'))), Q(flag=True),~Q(status='CO'), ~Q(status='NC'))
                elif request.GET.get('dates') != '' and request.GET.get('datee') != '':
                    model = CotKeys.objects.filter(Q(cotizacion__registrado__range=(globalVariable.format_str_date(request.GET.get('dates')),globalVariable.format_str_date(request.GET.get('datee')))), Q(flag=True),~Q(status='CO'), ~Q(status='NC'))
        else:
            model = CotKeys.objects.filter(Q(flag=True),~Q(status='CO'), ~Q(status='NC')).order_by('-cotizacion__registrado')

        paginator = Paginator(model, 15)
        page = request.GET.get('page')
        try:
            quote = paginator.page(page)
        except PageNotAnInteger:
            quote = paginator.page(1)
        except EmptyPage:
            quote = paginator.page(paginator.num_pages)
        context['list'] = quote
        if request.is_ajax():
            data = {}
            data['list'] = [{'cotizacion_id':x.cotizacion_id,'proveedor_id':x.proveedor_id,'razonsocial':x.proveedor.razonsocial,'keygen':x.keygen,'traslado':globalVariable.format_date_str(x.cotizacion.traslado)} for x in quote]
            data['status'] = True
            return HttpResponse(simplejson.dumps(data), mimetype='application/json')
        else:
            return render_to_response(self.template_name, context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                key = CotKeys.objects.get(cotizacion_id=request.POST.get('quote'),proveedor_id=request.POST.get('supplier'))
                if key.flag:
                    key.flag = False
                    key.save()
                flag = CotKeys.objects.filter(cotizacion_id=request.POST.get('quote'),proveedor_id=request.POST.get('supplier'), flag=True).aggregate(counter=Count('cotizacion'))
                if flag['counter'] == 0:
                    quote = Cotizacion.objects.get(cotizacion_id=request.POST.get('quote'))
                    quote.flag = False
                    quote.save()
                customer = CotCliente.objects.filter(cotizacion_id=request.POST.get('quote'),proveedor_id=request.POST.get('supplier'))
                if customer.__len__() > 0:
                    customer.flag = False
                    customer.save()
                context['status'] = True
            except ObjectDoesNotExist, e:
                raise e
                context['status'] = False
            return HttpResponse(simplejson.dumps(context), mimetype='application/json')

class ViewQuoteSingle(JSONResponseMixin, TemplateView):
    template_name = "logistics/single.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = super(ViewQuoteSingle, self).get_context_data(**kwargs)
        if request.is_ajax():
            if request.GET.get('type') == 'list':
                context = {}
                try:
                    tmp = tmpcotizacion.objects.filter(empdni=request.user.get_profile().empdni_id)
                    context['list'] = [{'id':x.id, 'materials_id':x.materiales_id, 'matname':x.materiales.matnom, 'matmeasure': x.materiales.matmed, 'unit':x.materiales.unidad_id, 'quantity':x.cantidad} for x in tmp]
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
        context['details'] = tmpcotizacion.objects.filter(empdni=request.user.get_profile().empdni_id).order_by('materiales__matnom')
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            if request.POST.get('type') == 'add':
                try:
                    form = addTmpCotizacionForm(request.POST)
                    if form.is_valid():
                        add = form.save(commit=False)
                        add.empdni = request.user.get_profile().empdni_id
                        add.save()
                        context['status'] = True
                    else:
                        context['status'] = False
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            if request.POST.get('type') == 'edit':
                try:
                    tmp = tmpcotizacion.objects.get(pk=request.POST.get('id'),materiales_id=request.POST.get('materials_id'))
                    tmp.cantidad = request.POST.get('quantity')
                    tmp.save()
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            if request.POST.get('type') == 'del':
                try:
                    tmp = tmpcotizacion.objects.get(pk=request.POST.get('id'),materiales_id=request.POST.get('materials_id'))
                    tmp.delete()
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            if request.POST.get('type') == 'delall':
                try:
                    tmp = tmpcotizacion.objects.filter(empdni=request.user.get_profile().empdni_id)
                    tmp.delete()
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            if request.POST.get('type') == 'read':
                try:
                    nothing = list()
                    # upload file
                    arch = request.FILES['archivo']
                    filename = uploadFiles.upload('/storage/temporary/', arch)
                    book = open_workbook(filename,encoding_override='utf-8')
                    sheet = book.sheet_by_index(0) # recover sheet of materials
                    for m in range(10, sheet.nrows):
                        mid = sheet.cell(m, 2)
                        if mid.ctype != XL_CELL_EMPTY:
                            mid = str(int(mid.value))
                        else:
                            mid = ''
                        cant = sheet.cell(m, 6) # get quantity
                        if len(mid) == 15: # row code is length equal 15 chars
                            obj, created = tmpcotizacion.objects.get_or_create(materiales_id=mid,empdni=request.user.get_profile().empdni_id,defaults={'cantidad':cant.value})
                            if not created:
                                obj.cantidad = (obj.cantidad + cant.value)
                                obj.save()
                        else:
                            if cant.ctype != XL_CELL_EMPTY:
                                nothing.append({'name':sheet.cell(m, 3).value, 'measure':sheet.cell(m, 4).value, 'unit':sheet.cell(m, 5).value, 'quantity': cant.value})
                            else:
                                continue
                    uploadFiles.removeTmp(filename)
                    context['status']= True
                    context['list'] = nothing
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            if request.POST.get('type') == 'addQuote':
                try:
                    if request.POST.get('check') == 'new':
                        quote = genkeys.GenerateKeyQuotation()
                        newQuote = True
                    elif request.POST.get('check') == 'old':
                        if request.POST.get('quote') == '':
                            quote = genkeys.GenerateKeyQuotation()
                            newQuote = True
                        else:
                            quote = request.POST.get('quote')
                            newQuote = False
                    if newQuote:
                        # Save quotation
                        obj = Cotizacion()
                        obj.cotizacion_id = quote
                        obj.empdni = request.user.get_profile().empdni_id
                        obj.almacen_id = request.POST.get('almacen')
                        obj.traslado = request.POST.get('traslado')
                        obj.obser = request.POST.get('obser')
                        obj.status = 'PE'
                        obj.flag = True
                        obj.save()

                    # Save Key Quotation for supplier
                    obj = CotKeys()
                    obj.cotizacion_id = quote
                    obj.proveedor_id = request.POST.get('proveedor')
                    obj.keygen = genkeys.GeneratekeysQuoteClient()
                    obj.status = 'PE'
                    obj.flag = True
                    obj.save()

                    # Save Details quotation for supplier
                    details = json.loads(request.POST.get('details'))
                    for x in details:
                        obj = DetCotizacion()
                        obj.cotizacion_id = quote
                        obj.proveedor_id = request.POST.get('proveedor')
                        obj.materiales_id = x['materials_id']
                        obj.cantidad = x['quantity']
                        obj.flag = True
                        obj.save()

                    context['quote'] = quote
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)

class ViewPurchaseSingle(JSONResponseMixin, TemplateView):
    template_name = "logistics/purchase.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.GET.get('type') == 'list':
                context = dict()
                try:
                    tmp = tmpcompra.objects.filter(empdni=request.user.get_profile().empdni_id)
                    context['list'] = []
                    igv = 0
                    subt = 0
                    total = 0
                    conf = Configuracion.objects.get(periodo=globalVariable.get_year)
                    tdiscount = 0
                    # print conf.igv
                    for x in tmp:
                        disc = ((x.precio * x.discount) / 100)
                        tdiscount += (disc * x.cantidad)
                        precio = x.precio - disc
                        amount = (x.cantidad * precio)
                        subt += amount
                        context['list'].append({'id':x.id, 'materials_id':x.materiales_id, 'matname':x.materiales.matnom, 'matmeasure': x.materiales.matmed, 'unit':x.materiales.unidad_id, 'quantity':x.cantidad, 'price':x.precio, 'discount':x.discount, 'amount':amount})
                    context['discount'] = tdiscount
                    context['igv'] = ((conf.igv * subt) / 100)
                    context['subtotal'] = subt
                    context['total'] = (context['igv'] + subt)
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
        context = super(ViewPurchaseSingle, self).get_context_data(**kwargs)
        context['document'] = Documentos.objects.all()
        context['pago'] = FormaPago.objects.all()
        context['currency'] = Moneda.objects.all()
        context['supplier'] = Proveedor.objects.all()
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            if request.POST.get('type') == 'add':
                try:
                    form = addTmpCompraForm(request.POST)
                    if form.is_valid():
                        add = form.save(commit=False)
                        add.empdni = request.user.get_profile().empdni_id
                        add.save()
                        context['status'] = True
                    else:
                        context['status'] = False
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            # if request.POST.get('type') == 'add':
            #     try:
            #         form = addTmpCompraForm(request.POST)
            #         if form.is_valid():
            #             add = form.save(commit=False)
            #             add.empdni = request.user.get_profile().empdni_id
            #             add.save()
            #             context['status'] = True
            #         else:
            #             context['status'] = False
            #     except ObjectDoesNotExist, e:
            #         context['raise'] = e
            #         context['status'] = False
            #     return self.render_to_json_response(context, **kwargs)
            if request.POST.get('type') == 'edit':
                try:
                    tmp = tmpcompra.objects.get(pk=request.POST.get('id'),materiales_id=request.POST.get('materials_id'))
                    tmp.cantidad = request.POST.get('quantity')
                    tmp.precio = request.POST.get('price')
                    tmp.discount = request.POST.get('discount')
                    tmp.save()
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            if request.POST.get('type') == 'del':
                try:
                    tmp = tmpcompra.objects.get(pk=request.POST.get('id'),materiales_id=request.POST.get('materials_id'))
                    tmp.delete()
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            if request.POST.get('type') == 'delall':
                try:
                    tmp = tmpcompra.objects.filter(empdni=request.user.get_profile().empdni_id)
                    tmp.delete()
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            if request.POST.get('type') == 'read':
                try:
                    nothing = list()
                    # upload file
                    arch = request.FILES['archivo']
                    filename = uploadFiles.upload('/storage/temporary/', arch)
                    book = open_workbook(filename,encoding_override='utf-8')
                    sheet = book.sheet_by_index(0) # recover sheet of materials
                    for m in range(10, sheet.nrows):
                        mid = sheet.cell(m, 2)
                        if mid.ctype != XL_CELL_EMPTY:
                            mid = str(int(mid.value))
                        else:
                            mid = ''
                        cant = sheet.cell(m, 6) # get quantity
                        price = sheet.cell(m, 7) # get price
                        if len(mid) == 15: # row code is length equal 15 chars
                            obj, created = tmpcompra.objects.get_or_create(materiales_id=mid,empdni=request.user.get_profile().empdni_id,defaults={'cantidad':cant.value,'precio':price.value})
                            if not created:
                                obj.cantidad = (obj.cantidad + cant.value)
                                obj.precio = price.value
                                obj.save()
                        else:
                            if cant.ctype != XL_CELL_EMPTY:
                                nothing.append({'name':sheet.cell(m, 3).value, 'measure':sheet.cell(m, 4).value, 'unit':sheet.cell(m, 5).value, 'quantity': cant.value, 'price':price.value})
                            else:
                                continue
                    uploadFiles.removeTmp(filename)
                    context['status']= True
                    context['list'] = nothing
                except ObjectDoesNotExist, e:
                    context['raise'] = e
                    context['status'] = False
                return self.render_to_json_response(context, **kwargs)
            # save to oreder purchase
            try:
                if 'savePurchase' in request.POST:
                    # Set all data the form
                    form = CompraForm(request.POST, request.FILES)
                    if form.is_valid():
                        id = genkeys.GenerateKeyPurchase()
                        add = form.save(commit=False)
                        add.compra_id = id
                        add.empdni_id = request.user.get_profile().empdni_id
                        add.status = 'PE'
                        add.save()
                        # save details os the order purchase
                        details = json.loads(request.POST.get('details'))
                        for x in details:
                            obj = DetCompra()
                            obj.compra_id = id
                            obj.materiales_id = x['materials']
                            obj.cantidad = x['quantity']
                            obj.precio = x['price']
                            obj.cantstatic = x['quantity']
                            obj.discount = x['discount']
                            obj.save()
                        # if all success delete all data of the temp purchase
                        obj = tmpcompra.objects.filter(empdni=request.user.get_profile().empdni_id)
                        obj.delete()
                        context['status'] = True
                        context['nro'] = id
                    else:
                        context['status'] = False
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

class ListPurchase(JSONResponseMixin, TemplateView):
    template_name = 'logistics/listPurchase.html'
    def get(self, request, *args, **kwargs):
        try:
            context = dict()
            if request.is_ajax():
                try:
                    if 'code' in request.GET:
                        context['list'] = [{'purchase' : x.compra_id, 'document' : x.documento.documento, 'transfer' :  globalVariable.format_date_str(x.traslado), 'currency' : x.moneda.moneda, 'deposito' : str(x.deposito)} for x in Compra.objects.filter(flag=True, pk=request.GET.get('code'))]
                    elif 'status' in request.GET:
                        context['list'] = [{'purchase' : x.compra_id, 'document' : x.documento.documento, 'transfer' :  globalVariable.format_date_str(x.traslado), 'currency' : x.moneda.moneda, 'deposito' : str(x.deposito)} for x in Compra.objects.filter(flag=True, status=request.GET.get('status'))]
                    elif 'dates' in request.GET:
                        if 'start' in request.GET and 'end' not in request.GET:
                            obj = Compra.objects.filter(flag=True, registrado__startswith=globalVariable.format_str_date(request.GET.get('start')))
                        elif 'start' in request.GET and 'end' in request.GET:
                            obj = Compra.objects.filter(flag=True, registrado__range=(globalVariable.format_str_date(request.GET.get('start')), globalVariable.format_str_date(request.GET.get('end'))))
                        context['list'] = [{'purchase':x.compra_id, 'document':x.documento.documento, 'transfer': globalVariable.format_date_str(x.traslado),'currency':x.moneda.moneda, 'deposito':str(x.deposito)} for x in obj]
                    context['status'] = True
                except ObjectDoesNotExist, e:
                    context['raise'] = e.__str__()
                    context['status'] = False
                return self.render_to_json_response(context)
            obj = Compra.objects.filter(status='PE', flag=True).order_by('-registrado')
            # paginator = Paginator(obj, 20)
            # page = request.GET.get('page')
            # try:
            #     purchase = paginator.page(page)
            # except PageNotAnInteger:
            #     purchase = paginator.page(1)
            # except EmptyPage:
            #     purchase = paginator.page(paginator.num_pages)
            context['purchase'] = obj
            return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        except TemplateDoesNotExist, e:
            raise Http404('Template not found')

class LoginSupplier(JSONResponseMixin, TemplateView):
    template_name = 'logistics/loginSupplier.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            if 'exists' in request.GET:
                exists = LoginProveedor.objects.filter(supplier_id=request.GET.get('ruc'))
                if exists:
                    context['exists'] = {'username':exists[0].username, 'status':True, 'supplier': exists[0].supplier_id}
                else:
                    context['exists'] = {'status' : False}
            return self.render_to_json_response(context)
        context['supplier'] = Proveedor.objects.filter(flag=True).order_by('razonsocial')
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax():
            try:
                if 'supplier' in request.POST:
                    obj = LoginProveedor.objects.filter(supplier_id=request.POST.get('supplier'))
                    passwd = request.POST.get('password')
                    passwd = hashlib.sha256(b'%s'%passwd)
                    passwd = passwd.hexdigest()
                    if obj:
                        obj[0].password = passwd
                        obj[0].save()
                    else:
                        obj = LoginProveedor()
                        obj.username = request.POST.get('username')
                        obj.password = passwd
                        obj.supplier_id = request.POST.get('supplier')
                        obj.save()
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return  self.render_to_json_response(context)

class SupplierCreate(CreateView):
    form_class = ProveedorForm
    model = Proveedor
    #success_url = reverse_lazy('proveedor_list')
    template_name = 'logistics/crud/supplier_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SupplierCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        #self.instance.save()
        form.save()
        return render_to_response(self.template_name, {'msg':'success'}, context_instance=RequestContext(self.request))

class CompareQuote(JSONResponseMixin, TemplateView):
    template_name = 'logistics/comparequote.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            context['quote'] = Cotizacion.objects.get(Q(cotizacion_id=kwargs['quote']), Q(flag=True), ~Q(status='CO'))
            context['supplier'] = CotKeys.objects.filter(cotizacion_id=kwargs['quote'])
            mats = DetCotizacion.objects.filter(cotizacion_id=kwargs['quote']).order_by('materiales__materiales_id').distinct('materiales__materiales_id')
            context['client'] = CotCliente.objects.filter(cotizacion_id=kwargs['quote'])
            context['conf'] = Configuracion.objects.get(periodo=globalVariable.get_year)
            arm = list()
            for x in mats:
                arr = list()
                data = dict()
                arsu = list()
                for j in context['supplier']:
                    dsup = DetCotizacion.objects.get(cotizacion_id=kwargs['quote'], proveedor_id=j.proveedor_id, materiales_id=x.materiales_id)
                    discount = (float(dsup.discount) / 100)
                    price = (dsup.precio - (float(dsup.precio) * discount))
                    amount = (price * float(x.cantidad))
                    arsu.append({'supplier':j.proveedor_id,'materiales_id':x.materiales_id, 'price':dsup.precio, 'discount': dsup.discount, 'brand':dsup.marca, 'model':dsup.modelo, 'amount':amount})
                    #data[j.proveedor_id] = arsu #{'price':dsup.precio, 'discount': dsup.discount, 'brand':dsup.marca, 'model':dsup.modelo}
                arr.append(data)
                arm.append({'materials':x.materiales_id, 'name': x.materiales.matnom, 'measure':x.materiales.matmed, 'unit': x.materiales.unidad.uninom, 'quantity':x.cantidad, 'others': arsu })
            context['details'] = arm
            context['currency'] = Moneda.objects.filter(flag=True)
            context['document'] = Documentos.objects.filter(flag=True)
            context['payment'] = FormaPago.objects.filter(flag=True)
            context['purchase'] = Compra.objects.filter(cotizacion_id=kwargs['quote'],flag=True)
            return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        except ObjectDoesNotExist, e:
            raise Http404

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = dict()
        if request.is_ajax:
            try:
                if 'purchase' in request.POST:
                    form = CompraForm(request.POST, request.FILES)
                    # print form.is_valid()
                    if form.is_valid():
                        add = form.save(commit=False)
                        purchase = genkeys.GenerateKeyPurchase()
                        add.compra_id = purchase
                        add.cotizacion_id = kwargs['quote']
                        add.flag = True
                        add.empdni_id = request.user.get_profile().empdni_id
                        add.save()
                        # save the details
                        details = json.loads(request.POST.get('details'))
                        # print details
                        for x in details:
                            # consult if brand exists and model
                            brand = Brand.objects.filter(brand__icontains=x['brand'])
                            if brand or x['brand'] == unicode(None):
                                if x['brand'] == unicode(None):
                                    brand = 'BR000'
                                else:
                                    brand = brand[0].brand_id
                            else:
                                br = Brand()
                                brand = genkeys.GenerateIdBrand()
                                br.brand_id = brand
                                br.brand = x['brand']
                                br.save()
                            # print brand
                            model = Model.objects.filter(model__icontains=x['model'])
                            if model or x['model'] == unicode(None):
                                if x['model'] == unicode(None):
                                    model = 'MO000'
                                else:
                                    model = model[0].model_id
                            else:
                                mo = Model()
                                model = genkeys.GenerateIdModel()
                                mo.model_id = model
                                mo.brand_id = brand
                                mo.model = x['model']
                                mo.save()
                            # print model
                            det = DetCompra()
                            det.compra_id = purchase
                            det.materiales_id = x['materials']
                            det.brand_id = brand
                            det.model_id = model
                            det.cantidad = x['quantity']
                            det.cantstatic = x['quantity']
                            det.precio = x['price']
                            det.discount = x['discount']
                            det.flag = '1'
                            det.save()
                        # change status of models CotCliente
                        try:
                            cust = CotCliente.objects.get(cotizacion_id=kwargs['quote'], proveedor_id=request.POST.get('proveedor'))
                            cust.status = "CO"
                            cust.save()
                        except ObjectDoesNotExist, e:
                            context['client'] = 'No change model CotClient'
                        # Change status of models CotKeys
                        try:
                            keys = CotKeys.objects.get(cotizacion_id=kwargs['quote'], proveedor_id=request.POST.get('proveedor'))
                            keys.status = "CO"
                            keys.save()
                        except ObjectDoesNotExist, e:
                            context['keys'] = 'No change model CotKeys'
                        context['purchase'] = purchase
                        context['status'] = True
                if 'finish' in request.POST:
                    cot = Cotizacion.objects.get(pk=kwargs['quote'])
                    cot.status = 'CO'
                    cot.save()
                    # change status of cotkeys and cot cli
                    keys = CotKeys.objects.filter(Q(cotizacion_id=kwargs['quote']), ~Q(status='CO'))
                    if keys:
                        for x in keys:
                            x.status = 'NC'
                            x.save()
                    cust = CotCliente.objects.filter(Q(cotizacion_id=kwargs['quote']), ~Q(status='CO'))
                    if cust:
                        for x in cust:
                            x.status = 'NC'
                            x.save()
                    context['status'] = True
            except ObjectDoesNotExist, e:
                context['raise']  = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)

class IngressPriceQuote(JSONResponseMixin, TemplateView):
    template_name = 'logistics/ingressprices.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            if kwargs['quote'] and kwargs['supplier']:
                if kwargs['quote'].__len__() == 10 and kwargs['supplier'].__len__() == 11:
                    context['quote'] = Cotizacion.objects.get(pk=kwargs['quote'])
                    if context['quote'].status != 'PE':
                        return HttpResponseRedirect(reverse_lazy('view_quote_list'))
                    else:
                        context['details'] = DetCotizacion.objects.filter(cotizacion_id=kwargs['quote'], proveedor_id=kwargs['supplier']).order_by('materiales__matnom')
                        obj = Configuracion.objects.filter(periodo=globalVariable.get_year)[:1]
                        context['igv'] = obj[0].igv
                        context['currency'] = Moneda.objects.filter(flag=True).order_by('moneda')
                        cli = CotCliente.objects.filter(cotizacion_id=kwargs['quote'], proveedor_id=kwargs['supplier'])
                        if cli:
                            if cli[0].status == 'CO':
                                context['disabled'] = True
                            else:
                                context['disabled'] = False
                        else:
                            context['disabled'] = False
                        context['supplier'] = kwargs['supplier']
                else:
                    return HttpResponseRedirect(reverse_lazy('view_quote_list'))
            else:
                return HttpResponseRedirect(reverse_lazy('view_quote_list'))
            return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        except TemplateDoesNotExist, e:
            raise Http404('Template not found')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            try:
                if 'blur' in request.POST:
                    obj = DetCotizacion.objects.get(cotizacion_id=kwargs['quote'], proveedor_id=kwargs['supplier'], materiales_id=request.POST.get('materials'))
                    if request.POST.get('blur') == 'price':
                        obj.precio = request.POST.get('val')
                        obj.save()
                        context['quantity'] = obj.cantidad
                        context['status'] = True
                    elif request.POST.get('blur') == 'desct':
                        obj.discount = request.POST.get('val')
                        obj.save()
                        context['quantity'] = obj.cantidad
                        context['status'] = True
                    elif request.POST.get('blur') == 'brands':
                        obj.marca = request.POST.get('val')
                        obj.save()
                        context['status'] = True
                    elif request.POST.get('blur') == 'models':
                        obj.modelo = request.POST.get('val')
                        obj.save()
                        context['status'] = True
                    elif request.POST.get('blur') == 'dates':
                        obj.entrega = globalVariable.format_str_date(request.POST.get('val'))
                        obj.save()
                        context['status'] = True
                if request.POST.get('type') == 'file':
                    sheet = request.FILES['sheet']
                    uri = '/storage/quotations/%s/%s/'%(kwargs['quote'], kwargs['supplier'])
                    name = '%s%s.pdf'%(uri, request.POST.get('materials'))
                    if uploadFiles.fileExists(name, True):
                        uploadFiles.deleteFile(name, True)

                    filename = uploadFiles.upload(uri, sheet, {'name':request.POST.get('materials')})
                    if filename:
                        context['status'] = True
                    else:
                        context['status'] = False
                if 'client' in request.POST:
                    obj = CotCliente.objects.filter(proveedor_id=kwargs['supplier'], cotizacion_id=kwargs['quote'])
                    if not obj:
                        obj = CotCliente()
                        obj.proveedor_id = kwargs['supplier']
                        obj.cotizacion_id = kwargs['quote']
                        obj.envio = globalVariable.format_str_date(request.POST.get('traslado'))
                        obj.validez = globalVariable.format_str_date(request.POST.get('validez'))
                        obj.contacto = request.POST.get('contacto')
                        obj.moneda_id = request.POST.get('moneda')
                        obj.obser = request.POST.get('obser')
                        obj.status = 'SD'
                        obj.flag = True
                        obj.save()
                        context['status'] = True
                        context['supplier'] = kwargs['supplier']
                        su = None
                        try:
                            su = Proveedor.objects.get(pk=kwargs['supplier'])
                            context['reason'] = su.razonsocial
                        except ObjectDoesNotExist, e:
                            su = 'Nothing'
                            print e
                        context['quote'] = kwargs['quote']
            except ObjectDoesNotExist, e:
                context['raise'] = e.__str__()
                context['status'] = False
            return self.render_to_json_response(context)