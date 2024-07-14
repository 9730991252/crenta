from django.shortcuts import render,redirect
from office.models import *
from order.models import *
from qr_code.models import *
from datetime import timedelta, date
from django.db.models import Q
# Create your views here.

def crenta_admin_dashboard(request):
    if request.session.has_key('crenta_admin_mobile'):
        pe=[]
        today_p=[]
        p=Product.objects.all()
        if p:
            for p in p:
                pid=p.id
                k=In_stock.objects.filter(product_id=pid,status=1).order_by('-id').first()
                if k:
                    pe.append(k)
                tp = In_stock.objects.filter(product_id=pid,date__gte=date.today(),date__lte=date.today()).order_by('-id').first()
                if tp:
                    today_p.append(tp)
                    #print(today_p)

        context={
            'pe':pe,
            'today_p':today_p,
            'pro':Product.objects.all()
        }
        return render(request,'crenta_admin/crenta_admin_dashboard.html',context)
    else:
        return render(request,'login.html')

def crenta_admin_logout (request):
    del request.session['crenta_admin_mobile']
    return redirect('/')

def old_stock(request):
    if request.session.has_key('crenta_admin_mobile'):
        context={}
        t=''
        d=''
        if 'Days'in request.POST:
            day = request.POST.get('day')
            if day == '0':
                pass
            else:
                d = (date.today() - timedelta(days=int(day)))
                t = In_stock.objects.filter(status=1,date__lte=d).order_by('product_id')[0:300]
            context={
                't':t,
                'd':d,
                'day':day,
            }
        return render(request,'crenta_admin/old_stock.html',context)
    else:
        return render(request,'login.html')
    


