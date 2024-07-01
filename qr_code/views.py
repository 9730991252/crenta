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
import datetime
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
        qr = ''
        if e:
            e=Employee.objects.get(employee_mobile=store_mobile)
            p=Product.objects.filter().all()
            for p in p:
                p_all_id=p.id
                tp = In_stock.objects.filter(product_id=p_all_id,date__gte=date.today(),date__lte=date.today()).order_by('-id').first()
                if tp:
                    tp_product.append(tp)
        if 'Tag_search' in request.POST:
            tag_num = request.POST.get('tag_number')
            qr_id = Qr_code.objects.filter(tag_number=tag_num).first()
            if qr_id:
                qn = Qr_code.objects.get(id=qr_id.id)
                if qn.in_status == 0:
                    qr = Qr_code.objects.get(id=qr_id.id)
                if qn.in_status == 1:
                    messages.warning(request,"Tag Allready Addded")
            else:
                messages.warning(request,"Rong Qr code")
        if 'Add_Production' in request.POST:
            em_id = request.POST.get('em_id')
            tag_id = request.POST.get('tag_id')
            qs = Qr_code.objects.get(id=tag_id)
            if int(qs.in_status) == 0 and int(qs.out_status) == 0:
                In_stock(
                    employee_id=em_id,
                    qr_code_id=qs.id,
                    product_id=qs.product_id,
                    tag_number=qs.tag_number,
                    status=1
                    ).save()
                qs.in_status=1
                qs.save()
        context={
            'e':e,
            'p':tp_product,
            'qr':qr,
        }
        return render(request,'store/in_poduct.html',context=context)        
    else:
        return redirect('login')
    
def out_product(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']     
        e=Employee.objects.filter(employee_mobile=store_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=store_mobile)
        context={
            'e':e,
        }
        if 'Add_voucher' in request.POST:
            creted_by = request.POST.get('e_id')
            voucher_name = request.POST.get('voucher_name')
            Voucher_name(
                creted_by_id=creted_by,
                name=voucher_name,
                verify_status = 0
            ).save()
            v = Voucher_name.objects.filter(creted_by_id=creted_by).last()
            return redirect(f'voucher_add_stock/{v.id}')
        
        return render(request,'store/out_poduct.html',context=context)        
    else:
        return redirect('login')
    
def voucher_add_stock(request, id):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']  
        op_product=[] 
        qr = ''  
        tag_num=''
        e=Employee.objects.filter(employee_mobile=store_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=store_mobile)
            v = Voucher_name.objects.get(id=id)
            p=Product.objects.filter().all()
            for p in p:
                p_all_id=p.id
                tp = Out_stock.objects.filter(product_id=p_all_id,voucher_id=id).order_by('-id').first()
                if tp:
                    op_product.append(tp)
        ps = Out_stock.objects.filter(voucher_id=id).order_by('product_id')
        if 'Tag_search' in request.POST:
            tag_num = request.POST.get('tag_number')
            qr_id = Qr_code.objects.filter(tag_number=tag_num).first()
            if qr_id:
                qn = Qr_code.objects.get(id=qr_id.id)
                if qn.out_status == 0:
                    qr = Qr_code.objects.get(id=qr_id.id)
                if qn.out_status == 1:
                    messages.warning(request,"Tag Allready Addded")
            else:
                messages.warning(request,"Rong Qr code")
        if 'Out_Product' in request.POST:
            qid = request.POST.get('tag_id')
            em_id = request.POST.get('em_id')
            v_id = request.POST.get('v_id')
            q = Qr_code.objects.get(id=qid)
            if int(q.in_status) == 1 and int(q.out_status) == 0:
                Out_stock(
                    employee_id=em_id,
                    qr_code_id=q.id,
                    product_id=q.product_id,
                    voucher_id=v_id,
                    tag_number=q.tag_number,
                    ).save()
                q.out_status=1
                q.save()
                return redirect(f'/qr_code/voucher_add_stock/{v_id}')
        context={
            'e':e,
            'v':v,
            'op':op_product,
            'ps':ps,
            'qr':qr,
            'tag_num':tag_num
        }
        return render(request,'store/voucher_add_stock.html',context=context)        
    else:
        return redirect('login')
    

def verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
        context={
            'e':e,
        }
        return render(request,'qr_code/verify_qr_code.html',context=context)        
    else:
        return redirect('login')

def pending_verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
        context={
            'e':e,
            'v':Voucher_name.objects.filter(verify_status=0)
        }
        return render(request,'qr_code/pending_verify_qr_code.html',context=context)        
    else:
        return redirect('login')
    

def accepted_verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
        context={
            'e':e,
            'v':Voucher_name.objects.filter(verify_status=1)
        }
        return render(request,'qr_code/accepted_verify_qr_code.html',context=context)        
    else:
        return redirect('login')
    
 

def pending_view_voucher(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            v = Voucher_name.objects.get(id=id)
            q = Out_stock.objects.filter(voucher_id=id)
            a = Out_stock.objects.filter(voucher_id=id,verify_status=1).count()
            b = Out_stock.objects.filter(voucher_id=id).count()
             
        if 'Verify' in request.POST:
            qid = request.POST.get('qid')
            q = Out_stock.objects.get(id=qid)
            if q.verify_status == 0:
                q.verify_status = 1
                q.verify_by = e.employee_name
                q.verify_date = datetime.datetime.now()
                q.save()
                return redirect(f'/qr_code/pending_view_voucher/{id}')
        if 'Voucher_Verify' in request.POST:
            v = Voucher_name.objects.get(id=id)
            v.verify_by = e.employee_name
            v.verify_status = 1
            v.verify_date = date.today()
            v.save()
            return redirect('/qr_code/pending_verify_qr_code')
        
        if 'Update_v' in request.POST:
            new_name_v = request.POST.get('new_name_v')
            vn = Voucher_name.objects.get(id=id)
            vn.name = new_name_v
            vn.save()
            return redirect(f'/qr_code/pending_view_voucher/{id}')
        context={
            'e':e,
            'q':q,
            'a':a,
            'b':b,
            'v':v
        }
        return render(request,'qr_code/pending_view_voucher.html',context=context)        
    else:
        return redirect('login')
    

def accepted_view_voucher(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            v = Voucher_name.objects.get(id=id)
            q = Out_stock.objects.filter(voucher_id=id)
        context={
            'e':e,
            'v':v,
            'q':q

        }
        return render(request,'qr_code/accepted_view_voucher.html',context=context)        
    else:
        return redirect('login')



