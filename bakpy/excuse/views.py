# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from excuse.models import Sdn, Blacklist, Whitelist
from django.contrib import messages

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
    #host = request.get_host()
    return render_to_response("index.html", locals())

def ui(request):
    return render(request,"ui.html")

def blank(request):
    return render(request,"blank.html")

def welcome(request):
    if 'user_name' in request.GET:
        messages.add_message(request, messages.INFO, 'GET USER NAME success!')
        return HttpResponse('Welcome!~'+request.GET['user_name'])
    else:
        return render_to_response('welcome.html',locals())

def whitelist(request):
        no = Whitelist.objects.count()
        if 'ok' in request.POST:
            messages.add_message(request, messages.INFO, 'get ok success')
            messages.success(request, 'Profile details updated.')
            wip = request.POST['wip']
            Whitelist.objects.create(no=no, address=wip)
            return HttpResponse('Successfully adding ' + wip)
        else:
            return render_to_response('whitelist.html',locals())
