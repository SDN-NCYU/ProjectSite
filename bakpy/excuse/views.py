# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from excuse.models import Sdn, Blacklist, Whitelist
from django.contrib import messages
from django.http import HttpResponseRedirect
import unicodedata

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
    messages.success(request, 'Profile details updated.', extra_tags='alert')
    return render(request,"blank.html")

def welcome(request):
    if 'user_name' in request.GET:
        return HttpResponse('Welcome!~'+request.GET['user_name'])
    else:
        return render_to_response('welcome.html',locals())

def whitelist(request):
        no = Whitelist.objects.count()
        whitelist = Whitelist.objects.all()
        errors=[]

        if 'ok' in request.POST:
            #messages.success(request, 'Profile details updated.', extra_tags='alert') # alert message
            wip = request.POST['wip']

            
            for i in range(0,no-1):
                w = unicodedata.normalize('NFKD', whitelist[i].address).encode('ascii','ignore') # convert unicode to string
                if wip == w:
                    errors.append('*** 此ip已存在名單中')
                    break

            if not errors:
                messages.success(request, 'Successfully added '+ wip , extra_tags='alert') 
                Whitelist.objects.create(no=no, address=wip)
                return render(request,'whitelist.html',locals())
            else:
                messages.success(request, 'Fail to added '+ wip , extra_tags='alert')
                return render(request,'whitelist.html',locals())
        else:
            return render(request,'whitelist.html',locals())
