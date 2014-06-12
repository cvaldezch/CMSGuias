#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

#######################
#  Variables Globals  #
#######################
"""
'PE' => "PENDING" # Pendiente
'AP' => "APPROVE" # Aprobado
'AN' => "ANNULAR" # Anulado
'IN' => "INCOMPLETE" # Incompleto
'CO' => "COMPLETE" # Completo
"""
status = {
    'PE' : "PENDIENTE", # Pendiente
    'AP' : "APROVADO", # Aprobado
    'AN' : "ANULAR", # Anulado
    'IN' : "INCOMPLETO", # Incompleto
    'CO' : "COMPLETO", # Completo
    'NN' : "Nothing" # Nothing
}

# types nipples
tipo_nipples= { "A": "Roscado", "B": "Ranurado", "C": "Roscado - Ranurado" }

# date now format str
def date_now(type='date',format="%Y-%m-%d"):
    date = datetime.datetime.today()
    if type == 'str':
        return "%s"%(date.strftime(format))
    elif type == 'date':
        return date.date()
    elif type == 'time':
        return date.date()
    else:
        return date