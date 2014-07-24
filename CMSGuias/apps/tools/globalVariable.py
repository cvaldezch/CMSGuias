#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from django.conf import settings

from django.contrib import messages
from django.http import Http404

#######################
#  Variables Globals  #
#######################
"""
    Status Models
"""
status = {
    'PE' : "PENDIENTE", # Pendiente
    'AP' : "APROBADO", # Aprobado
    'AN' : "ANULADO", # Anulado
    'IN' : "INCOMPLETO", # Incompleto
    'CO' : "COMPLETO", # Completo
    'NN' : "Nothing" # Nothing
}

# types nipples
tipo_nipples = { "A": "Roscado", "B": "Ranurado", "C": "Roscado - Ranurado" }

# date now format str
def date_now(type='date',format="%Y-%m-%d"):
    date = datetime.datetime.today()
    if type == 'str':
        return "%s"%(date.strftime(format))
    elif type == 'date':
        return date.date()
    elif type == 'time':
        return date.time()
    else:
        return date

# Convert Date str to Date and date to str
def format_date_str(_date=None, format="%Y-%m-%d"):
    date_str = ""
    try:
        if _date is not None:
            date_str = _date.strftime(format)
        else:
            date_str = "date invalid!"
    except Exception, e:
        messages.add_message("%s"%e)
        raise Http404
    return date_str

def format_str_date(_str=None, format="%Y-%m-%d"):
    str_date = ""
    try:
        if _str is not None:
            str_date = datetime.datetime.strptime(_str, format).date()
        else:
            str_date = "str invalid!"
    except Exception, e:
        print 'Error   '
        messages.add_message(e)
        raise Http404('Method Error')
    return str_date

# get year current
get_year = datetime.datetime.today().date().strftime("%Y")

# get Relative path
relative_path = settings.MEDIA_ROOT