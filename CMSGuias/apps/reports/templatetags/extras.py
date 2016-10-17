# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter(name='get_val')
def get_val(dictionary, args=''):
    ks = args.split(',')
    if (len(ks) > 1):
        if ks[0] in dictionary:
            return dictionary[ks[0]]
        else:
            return ks[1]
    else:
        ks = ks[0]
        if ks in dictionary:
            return dictionary[ks]
        else:
            return ''
