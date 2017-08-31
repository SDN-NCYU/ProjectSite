# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from excuse.models import Sdn, Blacklist, Whitelist, Dangersrc, Packetin
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime
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
    return render(request,"index.html", locals())

def ui(request):
    return render(request,"ui.html")

def blank(request):
    messages.success(request, 'Profile details updated.', extra_tags='alert')
    return render(request,"blank.html")

def NewProject(request):
    return render(request,"NewProject.html")

def mymodel(request):
    return render(request,"mymodel.html")

def Protect(request):
    entrop = Sdn.objects.all().order_by('time')
    no_entrop = Sdn.objects.count()
    myentrop = entrop[no_entrop-1].entropy
    myentrop_percent = (myentrop/5.0)*100
    myentrop_percent = str(myentrop_percent)

    packet = Packetin.objects.all().order_by('time')
    no_pack = Packetin.objects.count()
    mypacketin = packet[no_pack-1].packetin

    now = datetime.datetime.now().strftime('%H:%M:%S')

    #host = request.get_host()
    return render(request,"Protect.html", locals())

def whitelist(request):
    no = Whitelist.objects.count()
    whitelist = Whitelist.objects.all()
    errors=[]

    if 'ok' in request.POST:
        if('a' or 'b' or 'c' or 'd' not in request.POST):
            messages.success(request,'請輸入完整的ip', extra_tags='alert')
            return render(request,'whitelist.html',locals())
        elif(request.POST['a']>255 or request.POST['b']>255 or request.POST['c']>255 or request.POST['d']>255):
            messages.success(request,'請輸入值在0~255之間', extra_tags='alert')
            return render(request,'whitelist.html',locals())
        else:
            wip = request.POST['a']+"."+request.POST['b']+"."+request.POST['c']+"."+request.POST['d'] 
        
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
        return render(request,'index.html',locals())
