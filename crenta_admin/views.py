from django.shortcuts import render,redirect
from office.models import *
from order.models import *
from qr_code.models import *
from datetime import date

# Create your views here.

def crenta_admin_dashboard(request):
    if request.session.has_key('crenta_admin_mobile'):
        pe=[]
        p=Product.objects.all()
        if p:
            for p in p:
                pid=p.id
                k=In_stock.objects.filter(product_id=pid,status=1).order_by('-id').first()
                if k:
                    pe.append(k)
        context={
            'pe':pe,
        }
        return render(request,'crenta_admin/crenta_admin_dashboard.html',context)
    else:
        return render(request,'login.html')

def crenta_admin_logout (request):
    del request.session['crenta_admin_mobile']
    return redirect('/')

