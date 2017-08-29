# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from excuse.models import Sdn, Whitelist, Blacklist

# Register your models here.
admin.site.register(Whitelist)
