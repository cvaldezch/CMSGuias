#!/usr/python/env python
# -*- coding: utf-8 -*-

def RedirectModule(charge="administrator"):
    template_name = ""
    charge = unicode(charge)
    if charge == u"ADMINISTRATOR":
        template_name = "home/home.html"
    elif charge == u"Almacén":
        template_name = "almacen/storage.html"
    else:
        template_name = "warning.html"
    return template_name