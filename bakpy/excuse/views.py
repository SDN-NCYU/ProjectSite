# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from excuse.models import Sdn

def excuse(request):
    excuses = [
        "It was working in my head",
        "I thought I fixed that",
        "Actually, that is a feature",
        "It works on my machine",
    ]
    excuse = excuses[1]
    #return HttpResponse(excuses[1])
    return render(request, "index.html", {'excuse':excuse} )

def entropy(request):
    entrop = Sdn.objects.all()
    return render_to_response("index.html", locals())

