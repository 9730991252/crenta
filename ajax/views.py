from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from django.db.models import Sum
from django.db.models import Q
from office.models import *
from qr_code.models import *

# Create your views here.
def search_batch_product(request):
    if request.method == 'GET':
        words = request.GET['words']
        p=Product.objects.filter(product_name__icontains=words)
        context={
                's_p':p
        }
        t = render_to_string('ajax/search_batch_product.html', context)
    return JsonResponse({'data': t})



def add_new_batch(request):
    if request.method == 'GET':
        batch_name = request.GET['batch_name']
        eid = request.GET['eid']
        pid = request.GET['pid']
        sr = Batch.objects.filter(product_id=pid).count()
        sr += 1
        if batch_name == '':
            pass
        else:
            Batch(
                batch_name=batch_name,
                employee_id=eid,
                product_id=pid,
                sr_num=sr,
            ).save()
        b = Batch.objects.filter(product_id=pid)

        context={
            'b':b
        }
        t = render_to_string('ajax/batch_history.html', context)
    return JsonResponse({'data': t}) 



def search_qr_product(request):
    if request.method == 'GET':
        words = request.GET['words']
        p=Product.objects.filter(product_name__icontains=words)
        context={
                's_p':p
        }
        t = render_to_string('ajax/search_qr_product.html', context)
    return JsonResponse({'data': t})



def create_tage(request):
    if request.method == 'GET':
        f=''
        status = 0
        batch_id = request.GET['batch_id']
        eid = request.GET['eid']
        if batch_id:
            b = Batch.objects.get(id=batch_id)
            t = Qr_code.objects.filter(batch_id=batch_id,product_id=b.product_id).count()
            t += 1
            p_id = b.product_id
            f = f'{p_id}{batch_id}{t}'
            if int(t) < 1001:
                Qr_code(
                    product_id=b.product_id,
                    employee_id=eid,
                    batch_id=b.id,
                    tag_number=f,
                    sr_num=t
                    ).save()
            else:
                status = 1
            tag = Qr_code.objects.filter(batch_id=batch_id,product_id=b.product_id).last()
            qr = Qr_code.objects.filter(batch_id=batch_id).order_by('-id')
            if tag:
                tag = tag.tag_number
        context={
            'qr':qr
        }
        t = render_to_string('ajax/tag_list.html', context)
    return JsonResponse({'tag': tag,'status':status,'t':t}) 



def in_stock(request):
    if request.method == 'GET':
        tp_product=[]
        status = ''
        p_name = ''
        tag_num = request.GET['tag_num']
        em_id = request.GET['e_id']
        qr_id = Qr_code.objects.filter(tag_number=tag_num).first()
        if qr_id:
            qn = Qr_code.objects.get(id=qr_id.id)
            p_name = qn.product.product_name
            in_sta = qn.in_status
            if in_sta == 0:
                In_stock(
                    employee_id=em_id,
                    qr_code_id=qn.id,
                    product_id=qn.product_id,
                    tag_number=qn.tag_number,
                    status=1
                    ).save()
                qri = Qr_code.objects.get(id=qr_id.id)
                qri.in_status=1
                qri.save()
            p=Product.objects.filter().all()
            for p in p:
                p_all_id=p.id
                tp = In_stock.objects.filter(product_id=p_all_id).order_by('-id').first()
                if tp:
                    tp_product.append(tp)
                status = 1
            if in_sta == 1:
                status = 2
        else:
            status = 0
        context={
            'p':tp_product
                }
        t = render_to_string('ajax/today_production.html', context)
    return JsonResponse({'status': status,'t':t,'p_name':p_name})