from django.shortcuts import render, redirect
from office.models import *
from store.models import *
from marketing.models import *
# Create your views here.
def index(request):
    marketing_Cart.objects.all().delete()
    Marketing_order_detail.objects.all().delete()
    Marketing_order_master.objects.all().delete()
    return render(request, 'home/index.html')

def login(request):
    if request.session.has_key('office_mobile'):
        return redirect('office_home')
    if request.session.has_key('store_mobile'):
        return redirect('store_home')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            e= Office_employee.objects.filter(mobile=number,pin=pin,status=1)
            if e:
                request.session['office_mobile'] = request.POST["number"]
                return redirect('office_home')
            se= Store_employee.objects.filter(mobile=number,pin=pin,status=1)
            if se:
                request.session['store_mobile'] = request.POST["number"]
                return redirect('store_home')
    return render(request, 'home/login.html')

def marketing_login(request):
    if request.session.has_key('marketing_mobile'):
        return redirect('marketing_home')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            se= Marketing_employee.objects.filter(mobile=number,pin=pin,status=1)
            if se:
                request.session['marketing_mobile'] = request.POST["number"]
                return redirect('marketing_home')
    return render(request, 'home/login.html')


def sunil_login(request):
    if request.method == 'POST':
        a =int(request.POST["number"])
        b =int(request.POST["pin"])
        s = a+b
        if s == 10000 :
            request.session['sunil_mobile'] = s
            return redirect('add_employee_sunil')
        else:
            return redirect('sunil_login')
    return render(request,'home/sunil_login.html')

def office_logout(request):
    del request.session['office_mobile']
    return redirect('login')

def store_logout(request):
    del request.session['store_mobile']
    return redirect('login')