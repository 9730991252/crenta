from django.shortcuts import render ,redirect,HttpResponse
from office.models import *
from order.models import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
from django.core.paginator import Paginator
from django.db.models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        p='' 
        b='' 
        ba='' 
        pr='' 
        qr='' 
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
        if 'Select_Product' in request.POST:
            pid=request.POST.get('p_id')
            b = Batch.objects.filter(product_id=pid).order_by('-id')
            p=Product.objects.get(id=pid)
        if 'Select_Batch' in request.POST:
            bid = request.POST.get('bid')
            ba = Batch.objects.get(id=bid)
            pr = Product.objects.get(id=ba.product_id)
            qr = Qr_code.objects.filter(batch_id=bid).order_by('-id')
        context={
            'e':e,
            'p':p,
            'b':b,
            'pr':pr,
            'ba':ba,
            'qr':qr
        }
        return render(request,'qr_code/qr_code.html',context=context)        
    else:
        return redirect('login')
    



def in_product(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']     
        e=Employee.objects.filter(employee_mobile=store_mobile).first()
        tp_product=[]
        if e:
            e=Employee.objects.get(employee_mobile=store_mobile)
            p=Product.objects.filter().all()
            for p in p:
                p_all_id=p.id
                tp = In_stock.objects.filter(product_id=p_all_id).order_by('-id').first()
                if tp:
                    tp_product.append(tp)
        context={
            'e':e,
            'p':tp_product
        }
        return render(request,'store/in_poduct.html',context=context)        
    else:
        return redirect('login')