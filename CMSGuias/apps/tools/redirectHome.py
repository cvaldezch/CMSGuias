#!/usr/python/env python
# -*- coding: utf-8 -*-

def RedirectModule(charge='administrator'):
    template_name = ""
    charge = unicode(charge).upper()
    if charge == u'ADMINISTRATOR'.upper():
        template_name = 'home/home.html'
    elif charge == u'Almacen'.upper():
        template_name = 'almacen/storage.html'
    elif charge == u'Ventas'.upper():
        template_name = 'sales/home.html'
    elif charge == 'operaciones'.upper():
        template_name = 'operations/home.html'
    elif charge == 'logistica'.upper():
        template_name = 'logistics/home.html'
    else:
        template_name = 'warning.html'

    return template_name