from django.shortcuts import render
from office.models import *
from django.template.loader import render_to_string
from django.http import *
from office.models import *
from store.views import *
# Create your views here.
def generate_tag(request):
    if request.method == 'GET':
        tag_qty = request.GET['qty']
        eid = request.GET['eid']
        qr = Qr_code.objects.all().count()
        qr += 1
        for i in range (int(tag_qty)):
            Qr_code(
                employee_id=eid,
                tag_number=qr,
                ).save() 
            qr += 1
        tag = Qr_code.objects.filter().order_by('-id')[0:int(tag_qty)]
        context2={
            'tag_list':Qr_code.objects.filter().order_by('-id')[0:1000]
        }
        tag_list = render_to_string('ajax/office/tag_list.html', context2)
        context={
            'tag':tag
        }
        t = render_to_string('ajax/office/generate_tag.html', context)
    return JsonResponse({'t': t,'tag_list':tag_list})



def set_item_sr_num(request):
    if request.method == 'GET':
        num = request.GET['num']
        Item_id = request.GET['item_id']
        print(num)
        if num:
            item = Item.objects.get(id=Item_id)
            item.sr_num = num
            item.save()
    return JsonResponse({'t': 't'})



def search_in_item_ajax(request):
    if request.method == 'GET':
        words = request.GET['words']
        p = ''
        if words:
            p=Item.objects.filter(name__icontains=words)[0:10]
        context={
            'pro':p
        }
        t = render_to_string('ajax/store/search_in_item_ajax.html', context)
    return JsonResponse({'t': t})

def search_marketing_item_ajax(request):
    if request.method == 'GET':
        words = request.GET['words']
        p=Item.objects.filter(name__icontains=words)
        context={
            'item':p
        }
        t = render_to_string('ajax/marketing/search_marketing_item_ajax.html', context)
    return JsonResponse({'t': t})



def in_item(request):
    if request.method == 'GET':
        tag_number = request.GET['tag_num']
        employee_id = request.GET['e_id']
        batch_id = request.GET['b_id']
        item_id = request.GET['item_id']
        qr = Qr_code.objects.filter(tag_number=tag_number).first()
        if qr:
            qr_count = Qr_code.objects.filter(batch_id=batch_id).count()
            if qr_count < 1000:
                if qr.in_status == 0 and qr.out_status == 0:
                    #* success
                    in_item_save(tag_number,employee_id,item_id,batch_id,qr_count,scan_type=1)
                    status = 1
                if qr.in_status == 1:
                    #*Qr Code Already Scaned
                    status = 2
            else:
                #* create batch
                batch_save(item_id,employee_id)
                #* location reload
                status = 3
        else:
            #* Rong Qr Code
            status = 0
        item = Item.objects.get(id=item_id)
        i_name = item.name
        context={
            'i':item,
            'e':employee_id
                }
        t = render_to_string('ajax/store/today_production.html', context)
    return JsonResponse({'t':t, 'status':status, 'i_name':i_name}) 




def in_item_manual(request):
    if request.method == 'GET':
        tag_number = request.GET['tag_num']
        employee_id = request.GET['e_id']
        batch_id = request.GET['b_id']
        item_id = request.GET['item_id']
        qr = Qr_code.objects.filter(tag_number=tag_number).first()
        if qr:
            qr_count = Qr_code.objects.filter(batch_id=batch_id).count()
            if qr_count < 1000:
                if qr.in_status == 0 and qr.out_status == 0:
                    #* success
                    in_item_save(tag_number,employee_id,item_id,batch_id,qr_count,scan_type=0)
                    status = 1
                if qr.in_status == 1:
                    #*Qr Code Already Scaned
                    status = 2
            else:
                #* create batch
                batch_save(item_id,employee_id)
                #* location reload
                status = 3
        else:
            #* Rong Qr Code
            status = 0
        item = Item.objects.get(id=item_id)
        i_name = item.name
        context={
            'i':item,
            'e':employee_id
                }
        t = render_to_string('ajax/store/today_production.html', context)
    return JsonResponse({'t':t, 'status':status, 'i_name':i_name})


def in_item_save(tag_number,employee_id,item_id,batch_id,sr_num,scan_type):
    #print('tag_num = ',tag_number,  'eid = ',employee_id, 'item_id =', item_id,  'scan_type = ', scan_type)
    qr = Qr_code.objects.filter(tag_number=tag_number).first()
    sr_num += 1
    In_item(
        store_employee_id=employee_id,
        qr_code_id=qr.id,
        item_id=item_id,
        tag_number=tag_number,
        status=1,
        scan_type=scan_type,
    ).save()
    qr.in_status =1
    qr.batch_id = batch_id
    qr.item_id = item_id
    qr.sr_num = sr_num
    qr.save()

def search_tag(request):
    if request.method == 'GET':
        tag_num = request.GET['tag_num']
        item = ''
        i = Qr_code.objects.filter(tag_number=tag_num).first()
        if i:
            item = Qr_code.objects.filter(tag_number=tag_num).first()
        context={
            'i':item
               }
        t = render_to_string('ajax/store/serch_in_tag_result.html', context)
    return JsonResponse({'t':t}) 



def search_out_tag(request):
    if request.method == 'GET':
        tag_num = request.GET['tag_num']
        item = ''
        i = Qr_code.objects.filter(tag_number=tag_num).first()
        if i:
            item = Qr_code.objects.filter(tag_number=tag_num).first()
        context={
            'i':item
               }
        t = render_to_string('ajax/store/serch_out_tag_result.html', context)
    return JsonResponse({'t':t}) 



def out_item(request):
    if request.method == 'GET':
        status = ''
        i_name = ''
        vi_item = []
        tag_num = request.GET['tag_num']
        em_id = request.GET['e_id']
        v_id = request.GET['vid']
        if tag_num:
            qr = Qr_code.objects.filter(tag_number=tag_num).first()
            if qr:
                i_name = qr.item.name
                if qr.in_status == 1 and qr.out_status == 0:
                    #Out sucess
                    out_item_save(tag_num,em_id,v_id,scan_type=1)
                    it = Item.objects.all()
                    for i in it:
                        vi = Out_item.objects.filter(voucher_id=v_id,item_id=i.id).first()
                        if vi:
                            vi_item.append(vi)
                    status = 1
                if qr.in_status == 0:
                    #First Add Production
                    status = 2
                if qr.in_status == 1 and qr.out_status == 1:
                    #Already scaned
                    status = 3
            else:
                #Rong Qrcode
                status = 0
            context={
                'vi_item':vi_item
            }
        t = render_to_string('ajax/store/out_tag_list.html', context)
    return JsonResponse({'t':t,'status':status,'i_name':i_name}) 


def out_item_save(tag_num,em_id,v_id,scan_type):
    qr = Qr_code.objects.filter(tag_number=tag_num).first()
    if qr:
        Out_item(
            store_employee_id=em_id,
            qr_code_id=qr.id,
            item_id=qr.item_id,
            voucher_id=v_id,
            tag_number=tag_num,
            scan_type=scan_type,
        ).save()
        qr.out_status = 1
        qr.save()
        ins = In_item.objects.get(tag_number=tag_num)
        ins.status = 0
        ins.save()

def out_item_manual(request):
    if request.method == 'GET':
        status = ''
        i_name = ''
        vi_item = []
        tag_num = request.GET['tag_num']
        em_id = request.GET['e_id']
        v_id = request.GET['vid']
        if tag_num:
            qr = Qr_code.objects.filter(tag_number=tag_num).first()
            if qr:
                if qr.in_status == 1 and qr.out_status == 0:
                    i_name = qr.item.name
                    #Out sucess
                    out_item_save(tag_num,em_id,v_id,scan_type=0)
                    it = Item.objects.all()
                    for i in it:
                        vi = Out_item.objects.filter(voucher_id=v_id,item_id=i.id).first()
                        if vi:
                            vi_item.append(vi)
                    status = 1
                if qr.in_status == 0:
                    #First Add Production
                    status = 2
                if qr.in_status == 1 and qr.out_status == 1:
                    #Already scaned
                    status = 3
            else:
                #Rong Qrcode
                status = 0
            context={
                'vi_item':vi_item
            }
        t = render_to_string('ajax/store/out_tag_list.html', context)
    return JsonResponse({'t':t,'status':status,'i_name':i_name}) 


def search_item(request):
    if request.method == 'GET':
        words = request.GET['words']
        p = ''
        if len(words) > 2:
            p=Item.objects.filter(name__icontains=words)[0:10]
        context={
            'pro':p
        }
        t = render_to_string('ajax/office/search_item.html', context)
    return JsonResponse({'t': t})

def fetch_batch(request):
    if request.method == 'GET':
        pid = request.GET['pid']
        pro = Item.objects.get(id=pid)
        ba = Batch.objects.filter(item_id=pid)
        context={
            'pro':pro,
            'ba':ba
        }
        t = render_to_string('ajax/office/fetch_batch.html', context)
    return JsonResponse({'t': t})

def batch_detail(request):
    if request.method == 'GET':
        bid = request.GET['bid']
        ba = Batch.objects.get(id=bid)
        un_used = Qr_code.objects.filter(batch_id=bid,in_status=0).count()
        in_stock = Qr_code.objects.filter(batch_id=bid,in_status=1,out_status=0).count()
        out_stock = Qr_code.objects.filter(batch_id=bid,in_status=1,out_status=1).count()
        qr_code = Qr_code.objects.filter(batch_id=bid).order_by('-in_status' ,'out_status')

        context={
            'ba':ba,
            'un_used':un_used,
            'in_stock':in_stock,
            'out_stock':out_stock,
            'qr_code':qr_code
            }
        t = render_to_string('ajax/office/batch_detail.html', context)
    return JsonResponse({'t': t}) 