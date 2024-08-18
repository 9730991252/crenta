from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, date
import datetime
from store.models import *
# Create your views here.
def office_home(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        context={}
        ti_item = []
        all_stock_list = []
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            i=Item.objects.all()
            for i in i:
                ti = In_item.objects.filter(item_id=i.id,date__gte=date.today(),date__lte=date.today()).order_by('-id').first()
                if ti:
                    ti_item.append(ti)
                ########################
                s = In_item.objects.filter(item_id=i.id,status=1).first()
                print(s)
                if s:
                    all_stock_list.append(s)
        context={
            'e':e,
            't':ti_item,
            'all_stock_list':all_stock_list,

        }
        return render(request, 'office/office_home.html', context)
    else:
        return redirect('login')
    
def employee(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={
            'e':e,
        }
        return render(request, 'office/employee/employee.html', context)
    else:
        return redirect('login')

def office_employee(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            if 'add_office_employee'in request.POST:
                name=request.POST.get('name')
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                if Office_employee.objects.filter(mobile=mobile).exists():
                    messages.success(request,"Employee Allready Exits")
                else:
                    Office_employee(
                        name=name,
                        mobile=mobile,
                        pin=pin,
                        ).save()
                    messages.success(request,"Employee Add Succesfully") 
                    return redirect('office_employee')
            elif "Active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Office_employee.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Office_employee.objects.get(id=id)
                ac.status='1'
                ac.save() 
            elif "Edit" in request.POST:
                id=request.POST.get('id')
                name=request.POST.get('name')
                print(name)
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                #print(id)
                Office_employee(
                    id=id,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                ).save()
                messages.success(request,"Employee Edit Succesfully") 
                return redirect('/office/office_employee/')
        context={
            'e':e,
            'office_employee':Office_employee.objects.all()
        }
        return render(request, 'office/employee/office_employee.html', context)
    else:
        return redirect('login')
    
    
def store_employee(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            if 'add_store_employee'in request.POST:
                name=request.POST.get('name')
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                if Store_employee.objects.filter(mobile=mobile).exists():
                    messages.success(request,"Employee Allready Exits")
                else:
                    Store_employee(
                        name=name,
                        mobile=mobile,
                        pin=pin,
                        ).save()
                    messages.success(request,"Employee Add Succesfully") 
                    return redirect('store_employee')
            elif "Active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Store_employee.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Store_employee.objects.get(id=id)
                ac.status='1'
                ac.save() 
            elif "Edit" in request.POST:
                id=request.POST.get('id')
                name=request.POST.get('name')
                print(name)
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                #print(id)
                Store_employee(
                    id=id,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                ).save()
                messages.success(request,"Employee Edit Succesfully") 
                return redirect('/office/store_employee/')
        context={
            'e':e,
            'Store_employee':Store_employee.objects.all()
        }
        return render(request, 'office/employee/store_employee.html', context)
    else:
        return redirect('login')
    

@csrf_exempt
def generate_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            tag_list = Qr_code.objects.filter().order_by('-id')
            paginator = Paginator(tag_list,1000) 
            page_number = request.GET.get('page')
            tag_list = paginator.get_page(page_number)
            total_pages = tag_list.paginator.num_pages
        context={
            'e':e,
            'tag_list':tag_list,
            'last_page':total_pages,
            'total_page_list':[n+1 for n in range(total_pages)][0:3]
        }
        return render(request,'office/generate_qr_code.html',context=context)        
    else:
        return redirect('login')
    






def item(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={}

        if 'add_item'in request.POST:
            name=request.POST.get('name').upper()
            Item(
                name=name,
                employee_id=e.id
                ).save()
            messages.success(request,"Item Add Succesfully")
            return redirect('item')
        elif "Active" in request.POST:
            id=request.POST.get('id')
            #print(id)
            ac=Item.objects.get(id=id)
            ac.status='0'
            ac.save()
            return redirect('item')
        elif "Deactive" in request.POST:
            id=request.POST.get('id')
            #print(id)
            ac=Item.objects.get(id=id)
            ac.status='1'
            ac.save() 
            return redirect('item')

        elif "Edit" in request.POST:
            id=request.POST.get('id')
            name=request.POST.get('name').upper()
            #print(id)
            Item(
                id=id,
                name=name,
                employee_id=e.id
            ).save()
            messages.success(request,"Item Edit Succesfully") 
            return redirect('item')
    
        context={
            'e':e,
            'p':Item.objects.all().order_by('-sr_num')
        }
        return render(request, 'office/item.html', context)
    else:
        return redirect('login')



def verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={
            'e':e,
        }
        return render(request,'office/verify_qr_code.html',context=context)        
    else:
        return redirect('login')


def pending_verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={
            'e':e,
            'v':Voucher_name.objects.filter(verify_status=0)
        }
        return render(request,'office/pending_verify_qr_code.html',context=context)        
    else:
        return redirect('login')


 

def pending_view_voucher(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            v = Voucher_name.objects.get(id=id)
            q = Out_item.objects.filter(voucher_id=id).order_by('item_id')
            a = Out_item.objects.filter(voucher_id=id,verify_status=1).count()
            b = Out_item.objects.filter(voucher_id=id).count()
            if 'Verify' in request.POST:
                qid = request.POST.get('qid')
                q = Out_item.objects.get(id=qid)
                if q.verify_status == 0:
                    q.verify_status = 1 
                    q.verify_by_id = e.id
                    q.verify_date = datetime.datetime.now()
                    q.save()
                    return redirect(f'/office/pending_view_voucher/{id}')
            if 'Voucher_Verify' in request.POST:
                v = Voucher_name.objects.get(id=id)
                v.verify_by_id = e.id
                v.verify_status = 1
                v.verify_date = datetime.datetime.now()
                v.save()
                return redirect('/office/pending_verify_qr_code')
            
            if 'Update_v' in request.POST:
                new_name_v = request.POST.get('new_name_v')
                vn = Voucher_name.objects.get(id=id)
                vn.name = new_name_v
                vn.save()
                return redirect(f'/office/pending_view_voucher/{id}')
        context={
            'e':e,
            'q':q,
            'a':a,
            'b':b,
            'v':v
        }
        return render(request,'office/pending_view_voucher.html',context=context)        
    else:
        return redirect('login')
    


    

def accepted_verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            v = Voucher_name.objects.filter(verify_status=1)
            paginator = Paginator(v,10) 
            page_number = request.GET.get('page')
            v = paginator.get_page(page_number)
            total_pages = v.paginator.num_pages
        context={
            'e':e,
            'v': v,
            'last_page':total_pages,
            'total_page_list':[n+1 for n in range(total_pages)][0:3]
        }
        return render(request,'office/accepted_verify_qr_code.html',context=context)        
    else:
        return redirect('login')
    



    
def accepted_view_voucher(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            v = Voucher_name.objects.get(id=id)
            q = Out_item.objects.filter(voucher_id=id).order_by('item_id')
        context={
            'e':e,
            'v':v,
            'q':q

        }
        return render(request,'office/accepted_view_voucher.html',context=context)        
    else:
        return redirect('login')






