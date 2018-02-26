# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from excuse.models import Blacklist, Whitelist, Dangersrc, Packetin, Sdn, Sysstatus
from django.contrib import messages, auth
from datetime import datetime
import pytz
import unicodedata
import random
import json

ID_CHECK = "sdn"
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

def logintest(request):
    return render(request,"logintest.html")

def mymodel(request):
    return render(request,"mymodel.html")

def login(request):
    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/Protect.html/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    errors=[] 
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/Protect.html/')
    else:
        errors.append("Wrong Username or Password")
        return render(request,'login.html',locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('login.html')

def printaddr(lst, count):
    myaddr = []
    for i in range (0,count):
        addr = unicodedata.normalize('NFKD', lst[i].address).encode('ascii', 'ignore') #convert unicode to str
        myaddr.append(addr)
    myaddr = json.dumps(myaddr)
    return myaddr

def WhiteList(request):
    white = Whitelist.objects.all()
    count = Whitelist.objects.count()
    myaddr = []
    if 'dip' in request.POST:
        delete_data = request.POST.get('dip')
        ip = delete_data.split(',',2)
        ip = ip[1]
        white.filter(address = ip).delete()
        white = Whitelist.objects.all()
        count = Whitelist.objects.count()
        myaddr = printaddr(white, count)
        return render(request,'WhiteList.html',locals()) 
    else:
        myaddr = printaddr(white, count)

    if request.user.is_authenticated(): 
        return render(request,'WhiteList.html',locals()) 
    else:
    	return HttpResponseRedirect("/login.html/")

def BlackList(request):
    black = Blacklist.objects.all()
    count = Blacklist.objects.count()
    myaddr = []
    if 'dip' in request.POST:
        delete_data = request.POST.get('dip')
        ip = delete_data.split(',',2)
        ip = ip[1]
        black.filter(address = ip).delete()
        black = Blacklist.objects.all()
        count = Blacklist.objects.count()
        myaddr = printaddr(black, count)
        return render(request,'BlackList.html',locals()) 
    else:
        myaddr = printaddr(black, count)

    if request.user.is_authenticated(): 
        return render(request,'BlackList.html',locals()) 
    else:
    	return HttpResponseRedirect("/login.html/") 

def AttackList(request):
    attack = Dangersrc.objects.all()
    count = Dangersrc.objects.count()
    myaddr = []
    mytime = []
    for i in range (0,count):
        addr = unicodedata.normalize('NFKD', attack[i].address).encode('ascii','ignore') # convert unicode to string
        time = unicodedata.normalize('NFKD', attack[i].time).encode('ascii','ignore') # convert unicode to string
        mytime.append(time)
        myaddr.append(addr)
    mytime = json.dumps(mytime)
    myaddr = json.dumps(myaddr)

    if request.user.is_authenticated(): 
        return render(request,'AttackList.html',locals()) 
    else:
    	return HttpResponseRedirect("/login.html/") 

def Protect(request):
# -------------- DATA Visualize -----------------
    Status = Sysstatus.objects.all()
    no_status = Sysstatus.objects.count()
    mystatus = Status[no_status-1].status

    entrop = Sdn.objects.all().order_by('time')
    no_entrop = Sdn.objects.count()
    myentrop = entrop[no_entrop-1].entropy

    packet = Packetin.objects.all().order_by('time')
    no_pack = Packetin.objects.count()
    mypacketin = packet[no_pack-1].packetin

    tpe = pytz.timezone('Asia/Taipei')
    utcnow = datetime.utcnow()
    now = tpe.fromutc(utcnow).strftime('%H:%M:%S')

    errors=[]
    isValidUser = False 
    whitelist = Whitelist.objects.all().order_by('no')
    w_rows = Whitelist.objects.count()
    w_no = whitelist[w_rows-1].no + 1
    b_rows = Blacklist.objects.count()
    blacklist = Blacklist.objects.all().order_by("no")
    try:
        b_no = blacklist[b_rows-1].no + 1
    except:
        b_no = 0

    

    if 'IdCheck' in request.session:
        isValidUser = True
    elif isValidUser == False and 'pwd' in request.POST:
        password = request.POST.get('pwd')
        if(password != ID_CHECK):
            errors.append("*** Invalid Classification ***" )
            return render(request, 'Protect.html', locals())
        else:
            request.session['IdCheck'] = ID_CHECK

# -------------- Whitelist-Post Control  -----------------
    if 'w_ok' in request.POST:
        w1 = request.POST.get('w_first')
        w2 = request.POST.get('w_second')
        w3 = request.POST.get('w_third')
        w4 = request.POST.get('w_fourth')
        
        try:
            w1 = int(w1)
            w2 = int(w2)
            w3 = int(w3)
            w4 = int(w4)
        except ValueError:
            errors.append('*** Please Enter number')
            return render(request, 'Protect.html', locals())

        if(w1 > 255 or w2 > 255 or w3 > 255 or w4 > 255):
            errors.append('*** Please Enter the number between 0~255')
            return render(request, 'Protect.html', locals())
        else:
            wip = str(w1)+"."+str(w2)+"."+str(w3)+"."+str(w4)
        
        for i in range(0, w_rows):
            w = unicodedata.normalize('NFKD', whitelist[i].address).encode('ascii', 'ignore') # convert unicode to string
            if wip == w:
                errors.append('*** 此ip已存在名單中')
                break
        if not errors:
            messages.success(request, 'Successfully added '+ wip+ ' to whitelist', extra_tags='alert') 
            Whitelist.objects.create(no=w_no, address=wip)
            return render(request, 'Protect.html', locals())
        else:
            messages.success(request, 'Fail to added '+ wip, extra_tags='alert')
            return render(request, 'Protect.html', locals())

# -------------- Blacklist-Post Control  -----------------
    elif 'b_ok' in request.POST:
    	errors=[]
        
        b1 = request.POST.get('b_first')
        b2 = request.POST.get('b_second')
        b3 = request.POST.get('b_third')
        b4 = request.POST.get('b_fourth')
        
        try:
            b1 = int(b1)
            b2 = int(b2)
            b3 = int(b3)
            b4 = int(b4)
        except ValueError:
            errors.append('*** Please Enter number')
            return render(request, 'Protect.html', locals())

        if(b1 > 255 or b2 > 255 or b3 > 255 or b4 > 255):
            errors.append('*** Please Enter the number between 0~255')
            return render(request, 'Protect.html', locals())
        else:
            bip = str(b1)+"."+str(b2)+"."+str(b3)+"."+str(b4)
        
        for i in range(0, b_rows):
            b = unicodedata.normalize('NFKD', blacklist[i].address).encode('ascii', 'ignore') # convert unicode to string
            if bip == b:
                errors.append('*** 此ip已存在名單中')
                break
        if not errors:
            messages.success(request, 'Successfully added '+ bip+ ' to blacklist', extra_tags='alert') 
            Blacklist.objects.create(no=b_no, address=bip)
            return render(request, 'Protect.html', locals())
        else:
            messages.success(request, 'Fail to added '+ bip, extra_tags='alert')
            return render(request, 'Protect.html', locals())
    else:
	if request.user.is_authenticated(): 
        	return render(request,'Protect.html',locals()) 
    	else:
    		return HttpResponseRedirect("/Protect.html/") 
