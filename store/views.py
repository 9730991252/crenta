from django.shortcuts import render, redirect
from office.models import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import date
# Create your views here.
def store_home(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Store_employee.objects.filter(mobile=store_mobile,status=1).first()
        context={}
        if e:
            pass
        context={
            'e':e
        }
        return render(request, 'store/store_home.html', context)
    else:
        return redirect('login')
    
  
@csrf_exempt
def search_in_item(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Store_employee.objects.filter(mobile=store_mobile).first()
        in_stock_list = []
        if e:
            item = Item.objects.all().order_by('-sr_num')
            if item:
                for i in item:
                    i_name = In_item.objects.filter(item_id=i.id,date__gte=date.today(),date__lte=date.today()).first()
                    if i_name:
                        in_stock_list.append(i_name)
        context={
            'e':e,
            'in_stock_list':in_stock_list,
            'item':item
        }
        return render(request, 'store/search_in_item.html', context)
    else:
        return redirect('login')
    

def item_in(request,item_id):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Store_employee.objects.filter(mobile=store_mobile).first()
        context={}
        if e:
            b = Batch.objects.filter(item_id=item_id).count()
            if b == 0:
                batch_save(item_id,e.id)
                b_id = Batch.objects.filter(item_id=item_id).last()
            else:
                b_id = Batch.objects.filter(item_id=item_id).last()
        context={
            'e':e,
            'url_in':f'/store/item_in/{item_id}',
            'i':Item.objects.get(id=item_id),
            'b_id':b_id,
        }
        return render(request, 'store/item_in.html', context)
    else:
        return redirect('login')


def batch_save(item_id,e_id):
    b = Batch.objects.filter(item_id=item_id).count()
    b += 1
    Batch(
        item_id=item_id,
        in_employee_id=e_id,
        sr_num=b,
        batch_name=b,
    ).save()
    


def add_voucher(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Store_employee.objects.filter(mobile=store_mobile).first()
        context={}
        if e:
            if 'Add_voucher'in request.POST:
                voucher_name = request.POST.get('voucher_name')
                Voucher_name(
                    store_employee_id = e.id,
                    name = voucher_name,
                    verify_status = 0
                ).save()
                v = Voucher_name.objects.filter(store_employee_id=e.id).last()
                return redirect(f'/store/item_out/{v.id}')
        context={
            'e':e
        }
        return render(request, 'store/add_voucher.html', context)
    else:
        return redirect('login')


    
def item_out(request, id):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Store_employee.objects.filter(mobile=store_mobile,status=1).first()
        context={}
        vi_item = []
        if e:
            it = Item.objects.all()
            for i in it:
                vi = Out_item.objects.filter(voucher_id=id,item_id=i.id).first()
                if vi:
                    vi_item.append(vi)
        context={
            'e':e,
            'v':Voucher_name.objects.get(id=id),
            'out_url':f'/store/item_out/{id}',
            'vi_item':vi_item
        }
        return render(request, 'store/item_out.html', context)
    else:
        return redirect('login')












