#!/usr.bin/env python
# -*- coding: utf-8 -*-
#
from django.contrib import admin

from .models import *

admin.site.register(MetProject)
admin.site.register(SGroup)
admin.site.register(DSector)
admin.site.register(DSMetrado)