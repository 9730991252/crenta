from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, date
import datetime
from store.models import *
from marketing.models import *
import math
from django.db.models import Sum

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
    
@csrf_exempt
def view_pending_order(request, marketing_employee_id, dealer_id):

    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
            if 'add_item_to_cart'in request.POST:
                item_id = request.POST.get('item_id')
                qty = request.POST.get('qty')
                price = request.POST.get('price')
                marketing_Cart(
                    marketing_employee_id = marketing_employee_id,
                    accepted_by=e,
                    dealer_id=dealer_id,
                    item_id=item_id,
                    qty=qty,
                    price=float(price),                    
                    total_amount=(float(qty) * float(price)),
                    status='Accepted'
                ).save()
                messages.success(request, 'New Item Added successfuly')
                return redirect('view_pending_order', marketing_employee_id, dealer_id)
            if 'complete_order' in request.POST:
                odate = request.POST.get('date')
                # Aggregate total amount from cart
                total_price = marketing_Cart.objects.filter(
                    marketing_employee_id=marketing_employee_id,
                    dealer_id=dealer_id,
                    status='Accepted'  # Assuming you only want accepted items
                ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

                # Create new order master entry
                order_filter = Marketing_order_master.objects.count() + 1
                order_master = Marketing_order_master.objects.create(
                    marketing_employee_id=marketing_employee_id,
                    accepted_id=e.id,
                    dealer_id=dealer_id,
                    total_price=total_price,
                    order_filter=order_filter,
                    status='Accepted',
                    date=odate,
                )

                # Loop through all items that are active (status=1)
                for item in Item.objects.filter(status=1):
                    # Filter cart entries for this item with 'Accepted' status
                    cart_items = marketing_Cart.objects.filter(
                        marketing_employee_id=marketing_employee_id,
                        dealer_id=dealer_id,
                        item_id=item.id,
                        status='Accepted'
                    )

                    if cart_items.exists():
                        total_qty = cart_items.aggregate(Sum('qty'))['qty__sum'] or 0
                        total_item_price = cart_items.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
                        first_cart = cart_items.first()  # To get price info

                        # Create order detail entry
                        Marketing_order_detail.objects.create(
                            order_master=order_master,
                            item=item,
                            qty=total_qty,
                            price=first_cart.price,
                            total_price=total_item_price,
                            order_filter=order_filter,
                            item_name=item.name
                        )

                # Clear accepted items from cart
                marketing_Cart.objects.filter(
                    marketing_employee_id=marketing_employee_id,
                    dealer_id=dealer_id,
                    status='Accepted'
                ).delete()

                # Redirect to accepted order view
                return redirect(f'/office/view_accepted_order/{order_master.id}/')

            if 'change_price'in request.POST:
                t_id = request.POST.get('id')
                t_price = request.POST.get('price')
                od = marketing_Cart.objects.filter(id=t_id).first()
                od.price = t_price
                od.total_amount = float(od.qty) * float(t_price)
                od.save()
                messages.success(request, 'Price changed successfuly')
                return redirect('view_pending_order', marketing_employee_id, dealer_id)
                
                
            if 'change_qty'in request.POST:
                t_id = request.POST.get('id')
                t_qty = request.POST.get('qty')
                oc = marketing_Cart.objects.filter(id=t_id).first()
                oc.qty = t_qty
                oc.total_amount = float(t_qty) * oc.price
                oc.save()
                messages.success(request, 'Qty changed successfuly')
                return redirect('view_pending_order', marketing_employee_id, dealer_id)
                
            if 'Delete'in request.POST:
                t_id = request.POST.get('id')
                o = marketing_Cart.objects.filter(id=t_id).delete()
                messages.error(request, 'Item Deleted successfuly')
                return redirect('view_pending_order', marketing_employee_id, dealer_id)
            
            if 'Accept'in request.POST:
                id = request.POST.get('id')
                oc = marketing_Cart.objects.filter(id=id).first()
                oc.status = 'Accepted'
                oc.accepted_by = e
                oc.save()
                messages.success(request, 'Order Accepted')
                return redirect('view_pending_order', marketing_employee_id, dealer_id)
            
            pending_total = marketing_Cart.objects.filter(marketing_employee_id=marketing_employee_id, dealer_id=dealer_id, status='Pendding').aggregate(Sum('total_amount'))['total_amount__sum']
            accepted_total = marketing_Cart.objects.filter(marketing_employee_id=marketing_employee_id, dealer_id=dealer_id, status='Accepted').aggregate(Sum('total_amount'))['total_amount__sum']
        context={
            'e':e,
            'dealer':Dealer.objects.filter(id=dealer_id).first(),
            'marketing_employee':Marketing_employee.objects.filter(id=marketing_employee_id).first(),
            'pending_cart':marketing_Cart.objects.filter(marketing_employee_id=marketing_employee_id, dealer_id=dealer_id, status='Pendding'),
            'accepted_cart':marketing_Cart.objects.filter(marketing_employee_id=marketing_employee_id, dealer_id=dealer_id, status='Accepted'),
            'accepted_total':accepted_total,
            'pending_total':pending_total
            }
        return render(request, 'office/view_pending_order.html', context)
    else:
        return redirect('login')
    
def view_accepted_order(request, id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            om = Marketing_order_master.objects.filter(id=id).first() or ''
        context={
            'e':e,
            'om':om,
            'od':Marketing_order_detail.objects.filter(order_master=om)
            }
        return render(request, 'office/view_accepted_order.html', context)
    else:
        return redirect('login')
    
def order(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={
            'e':e,
        }
        return render(request, 'office/order.html', context)
    else:
        return redirect('login')
    
def pending_order(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            m_cart = []
            for em in Marketing_employee.objects.filter(status=1):
                if marketing_Cart.objects.filter(marketing_employee=em).exists():
                    for d in Dealer.objects.filter(status=1):
                        c = marketing_Cart.objects.filter(marketing_employee=em, dealer=d).first()
                        if c:
                            m_cart.append({
                                'marketing_employee':em,
                                'dealer':c.dealer,
                                'date':c.date
                            })
        m_cart.sort(key=lambda x: x['marketing_employee'].id)
        context={
            'e':e,
            'm_cart':m_cart,
        }
        return render(request, 'office/pending_order.html', context)
    else:
        return redirect('login')
    
def accepted_order(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={
            'e':e,
            'om':Marketing_order_master.objects.filter(status='Accepted'),
        }
        return render(request, 'office/accepted_order.html', context)
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
    
def marketing_employee(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            return_name = ''
            return_mobile = ''
            if 'add_marketing_employee'in request.POST:
                name=request.POST.get('name')
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                if name == '':
                    messages.error(request,"Please Enter Name")
                elif mobile == '':
                    messages.error(request,"Please Enter Mobile Number")
                elif Marketing_employee.objects.filter(mobile=mobile).exists():
                    messages.error(request,"Employee Allready Exits")
                else:
                    Marketing_employee(
                        added_by_id=e.id,
                        name=name,
                        mobile=mobile,
                        pin=pin or str('0000'),
                        ).save()
                    messages.success(request,"Employee Add Succesfully") 
                    return redirect('marketing_employee')
                return_name = request.POST.get('name')
                return_mobile = request.POST.get('mobile')
            elif "Active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Marketing_employee.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Marketing_employee.objects.get(id=id)
                ac.status='1'
                ac.save() 
            elif "Edit" in request.POST:
                id=request.POST.get('id')
                name=request.POST.get('name')
                print(name)
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                #print(id)
                Marketing_employee(
                    id=id,
                    added_by_id=e.id,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                ).save()
                messages.success(request,"Employee Edit Succesfully") 
                return redirect('/office/marketing_employee/')
        context={
            'e':e,
            'marketing_employee':Marketing_employee.objects.all(),
            'return_name': return_name,
            'return_mobile': return_mobile,
        }
        return render(request, 'office/employee/marketing_employee.html', context)
    else:
        return redirect('login')
    
def dealer(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            return_name = ''
            return_mobile = ''
            if 'add_dealer'in request.POST:
                name=request.POST.get('name').upper()
                if name == '':
                    messages.error(request,"Please Enter Name")
                elif Dealer.objects.filter(name=name).exists():
                    messages.error(request,"Dealer Allready Exits")
                else:
                    Dealer(
                        added_by_office_id=e.id,
                        name=name,
                        ).save()
                    messages.success(request,"dealer  Add Succesfully") 
                    return redirect('dealer')
                return_name = request.POST.get('name')
                return_mobile = request.POST.get('mobile')
            elif "Active" in request.POST:
                id=request.POST.get('id')
                ac=Dealer.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Deactive" in request.POST:
                id=request.POST.get('id')
                ac=Dealer.objects.get(id=id)
                ac.status='1'
                ac.save() 
            elif "Edit" in request.POST:
                id=request.POST.get('id')
                name=request.POST.get('name').upper()
                if name == '':
                    messages.error(request,"Please Enter Name")
                elif Dealer.objects.filter(name=name).exists() and Dealer.objects.get(name=name).id != int(id):
                    messages.error(request,"Dealer Allready Exits")
                else:
                    Dealer(
                        id=id,
                        added_by_office_id=e.id,
                        name=name,
                    ).save()
                    messages.success(request,"dealer Edit Succesfully") 
                return redirect('/office/dealer/')
        context={
            'e':e,
            'dealer':Dealer.objects.all(),
            'return_name': return_name,
            'return_mobile': return_mobile,
        }
        return render(request, 'office/dealer.html', context)
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
            'total_page_list':[n+1 for n in range(total_pages)][0:3],
            'un_used_tag':Qr_code.objects.filter(in_status=0, out_status=0).count()
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
        qr_code=[]
        if e:
            v = Voucher_name.objects.get(id=id)
            q = Out_item.objects.filter(voucher_id=id).order_by('item_id')
            a = Out_item.objects.filter(voucher_id=id,verify_status=1).count()
            b = Out_item.objects.filter(voucher_id=id).count()
            item=Item.objects.all()
            if item:
                for item in item:
                    item_id=item.id
                    qr_code_raw = Out_item.objects.filter(voucher_id=id,item_id=item_id).first()
                    if qr_code_raw:
                       qr_code.append(qr_code_raw)    
            if 'Verify' in request.POST:
                item_id_v = request.POST.get('item_id')
                q = Out_item.objects.filter(voucher_id=id,item_id=item_id_v)
                if q :
                    for q in q :
                        if q.verify_status == 0:
                            q.verify_status = 1
                            q.verify_by_id = e.id
                            q.verify_date = datetime.datetime.now() 
                            q.save()
                return redirect(f'/office/pending_view_voucher/{id}')

                #if q.verify_status == 0:
                    #q.verify_status = 1 
                    #q.verify_by_id = e.id
                    #q.verify_date = datetime.datetime.now()
                    #q.save()
                    #print(q.verify_status)
                    #return redirect(f'/office/pending_view_voucher/{id}')
                    #pass
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
            'q':qr_code,
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






