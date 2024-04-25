from django.shortcuts import render ,redirect
from order.models import *
from office.models import *
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
from django.core.paginator import Paginator

# Create your views here.
def order(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        stock=[]
        product=[]
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
        context={
            'e':e
        }
        return render(request,'order/order.html',context=context)
    else:
        return redirect('login')
    


def marketing_dashboard(request):
    if request.session.has_key('marketing_mobile'):
        marketing_mobile = request.session['marketing_mobile']        
        context={}
        stock=[]
        d=[]
        e=Employee.objects.filter(employee_mobile=marketing_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=marketing_mobile)
        if "Search" in request.GET:
            search_dealer = request.GET.get('search_dealer')
            dl=len(search_dealer)
            print(search_dealer)
            if 2<dl:
                d=Dealer.objects.filter(dealer_shope_name__icontains=search_dealer)
                d=d
                print(d)
        context={
            'e':e,
            'd':d
        }
        return render(request,'marketing/marketing_dashboard.html',context=context)
    else:
        return redirect('login')
    



def order_master_marketing(request):
    if request.session.has_key('marketing_mobile'):
        marketing_mobile = request.session['marketing_mobile']        
        context={}

        e=Employee.objects.filter(employee_mobile=marketing_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=marketing_mobile)
            o=OrderMaster.objects.filter(marketing_employee_id=e.id)

        context={
            'e':e,
            'o':o
        }
        return render(request,'marketing/order_master_marketing.html',context=context)
    else:
        return redirect('login')
    




def marketing_add_order(request,id):
    if request.session.has_key('marketing_mobile'):
        marketing_mobile = request.session['marketing_mobile']        
        context={}
        stock=[]
        d=[]
        e=Employee.objects.filter(employee_mobile=marketing_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=marketing_mobile)
            d=Dealer.objects.get(id=id)
            product=Cart.objects.filter(dealer_id=id)
            all_qty=Cart.objects.filter(dealer_id=id).count()
        a_c=Cart.objects.filter(dealer_id=id)
        total_amount=0
        if a_c:
            for a in a_c:
                t=a.total_price
                total_amount+=t

        if "Delete" in request.POST:
            cart_id=request.POST.get('cart_id')
            Cart.objects.get(id=cart_id).delete()
            return redirect(f'/order/marketing_add_order/{id}') 
        elif "Place_order" in request.POST:
            f=OrderMaster.objects.filter().count()
            f+=1
            OrderMaster(
                dealer_id=d.id,
                marketing_employee_id=e.id,
                status ='Pending',
                total_price=total_amount,
                order_filter=f
                ).save()
            c=Cart.objects.filter(dealer_id=id)
            if c:
                for c in c:
                    i=c.id
                    print(i)
                    Order_detail(
                        dealer_id=d.id,
                        marketing_employee_id=e.id,
                        product_id=c.product_id,
                        product_name=c.product.product_name,
                        category=c.category,
                        type=c.type,
                        order_filter=f,
                        qty=c.qty,
                        price=c.price
                        ).save()
                    Cart.objects.filter(dealer_id=id).delete()
            return redirect(f'/order/marketing_dashboard/')
        context={
            'e':e,
            'd':d,
            'product':product,
            'all_qty':all_qty,
            'total_amount':total_amount
        }
        return render(request,'marketing/marketing_add_order.html',context=context)
    else:
        return redirect('login')
    


def product_filter(request):
    if request.method == 'GET':
        words = request.GET['words']
        product=[]
        l=len(words)

        if 1<l:
            p=Product.objects.values().filter(product_name__icontains=words)
            product=list(p)
            #print(p)               
            return JsonResponse({'status': 1,'product':product})
    else:
        return JsonResponse({'status': 0})

def add_to_cart(request):
    if request.method == 'GET':
        employee_id = request.GET['employee_id']
        dealer_id = request.GET['dealer_id']
        product_id = request.GET['product_id']
        price = request.GET['price']
        #print('hi',type(price))
        p=Product.objects.get(id=product_id)
        qty = request.GET['qty']
        if Cart.objects.filter(dealer_id=dealer_id,employee_id=employee_id,product_id=product_id).exists():
            c=Cart.objects.get(dealer_id=dealer_id,employee_id=employee_id,product_id=product_id)
            c.qty=qty
            c.price=price
            c.save()
        else:
            Cart(
                dealer_id=dealer_id,
                employee_id=employee_id,
                product_id=p.id,
                product_name=p.product_name,
                category=p.category,
                type=p.type,
                qty=qty,
                price=price
            ).save()
        product=Cart.objects.values().filter(dealer_id=dealer_id)
        cart=list(product)
        ng=len(product)
        t=Cart.objects.filter(dealer_id=dealer_id)
        total_amount=0
        if t:
            for t in t:
                t=t.total_price
                total_amount+=t        
        return JsonResponse({'status': 1,'cart':cart,'ng':ng,'total_amount':total_amount})
    else:
        return JsonResponse({'status': 0})



def remove_cart_marketing(request):
    if request.method == 'GET':
        id = request.GET['id']
        if Cart.objects.filter(id=id).exists():
                Cart.objects.get(id=id).delete()
        return JsonResponse({'status': 1,})
    else:
        return JsonResponse({'status': 0})




def pending_order(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            pending=OrderMaster.objects.filter(status='Pending').order_by('-id')

        context={
            'e':e,
            'pending':pending
        }
        return render(request,'order/pending_order.html',context=context)
    else:
        return redirect('login')





def accepted_order(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            accepted=OrderMaster.objects.filter(status='Accepted').order_by('-id')

        context={
            'e':e,
            'accepted':accepted
        }
        return render(request,'order/accepted_order.html',context=context)
    else:
        return redirect('login')
    


def cancel_order(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            cancel=OrderMaster.objects.filter(status='Cancel').order_by('-id')

        context={
            'e':e,
            'cancel':cancel
        }
        return render(request,'office/cancel_order.html',context=context)
    else:
        return redirect('login')
    





def pending_view_order(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        stock=[]
        d={}
        order_filter=id
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            oms=OrderMaster.objects.get(order_filter=id)
            count_cancel=Order_detail.objects.filter(order_filter=order_filter,stock_status=2).count()
            acpt_order=Order_detail.objects.filter(order_filter=order_filter,stock_status= 1).count()
            acpt_order+=count_cancel
            #print(acpt_order)
            total=0
            am_order=Order_detail.objects.filter(order_filter=order_filter,stock_status=1)
            if am_order:
                for am in am_order:
                    t=am.total_price
                    total+=t
            order=Order_detail.objects.filter(order_filter=order_filter)
            if order :
                for p in order:
                    d_id=p.dealer_id
                    product_id=p.product_id
                    s=Stock_Product.objects.filter(product_id=product_id).order_by('-id').first()
                    if s:
                        stock.append(s)
                        #print(stock)                      
                d=Dealer.objects.get(id=d_id)
                if d:
                    d=d
        if "Accepte" in request.POST:
            order_detail_id=request.POST.get('order_detail_id')
            p=Order_detail.objects.get(id=order_detail_id)
            s=Stock_Product.objects.filter(product_id=p.product_id).order_by('-id').first()
            if s is not None:
                stock_qty=s.stock_qty
                odqty=p.qty
                if odqty<stock_qty:
                    Sell_Product(
                        dealer_id=p.dealer_id,
                        product_id=p.product_id,
                        employee_id=e.id,
                        qty=odqty,
                    ).save()
                    p.stock_status=1
                    p.save()
                    return redirect(f'/order/pending_view_order/{id}')
        elif "Out_of_stock" in request.POST:
            order_detail_id=request.POST.get('order_detail_id')
            p=Order_detail.objects.get(id=order_detail_id)
            p.stock_status=2
            p.save()
            return redirect(f'/order/pending_view_order/{id}')
        elif "Cancel_order" in request.POST:
            order_master_id=request.POST.get('order_master_id')
            r=OrderMaster.objects.get(id=order_master_id)
            r.status='Cancel'
            r.save()
            return redirect('/order/pending_order/')            
        elif "Accepte_order" in request.POST:
            order_master_id=request.POST.get('order_master_id')
            r=OrderMaster.objects.get(id=order_master_id)
            r.status='Accepted'
            r.save()
            return redirect('/order/pending_order/')            
        context={
            'e':e,
            'o':order,
            'd':d,
            'total':total,
            'stock':stock,
            'oms':oms,
            'count_cancel':count_cancel,
            'acpt_order':acpt_order
        }
        return render(request,'order/pending_view_order.html',context=context)        
    else:
        return redirect('login')
    




def accepted_view_order(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        stock=[]
        d={}
        order_filter=id
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            oms=OrderMaster.objects.get(order_filter=id)
            #print(oms)
            total=0
            am_order=Order_detail.objects.filter(order_filter=order_filter,stock_status=1)
            if am_order:
                for am in am_order:
                    t=am.total_price
                    total+=t
            order=Order_detail.objects.filter(order_filter=order_filter,stock_status=1)
            if order :
                for p in order:
                    d_id=p.dealer_id
                    product_id=p.product_id
                    s=Stock_Product.objects.filter(product_id=product_id).order_by('-id').first()
                    if s:
                        stock.append(s)
                        #print(stock)                      
                d=Dealer.objects.get(id=d_id)
                if d:
                    d=d

        elif "Cancel_order" in request.POST:
            order_master_id=request.POST.get('order_master_id')
            r=OrderMaster.objects.get(id=order_master_id)
            r.status='Cancel'
            #r.save()
            return redirect('/order/pending_order/')
            
        context={
            'e':e,
            'o':order,
            'd':d,
            'total':total,
            'stock':stock,
            'oms':oms
        }
        return render(request,'order/accepted_view_order.html',context=context)        
    else:
        return redirect('login')
    


def cancel_view_order(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        stock=[]
        d={}
        order_filter=id
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            oms=OrderMaster.objects.get(order_filter=id)
            #print(oms)
            total=0
            am_order=Order_detail.objects.filter(order_filter=order_filter,stock_status=2)
            if am_order:
                for am in am_order:
                    t=am.total_price
                    total+=t
            order=Order_detail.objects.filter(order_filter=order_filter,stock_status=2)
            if order :
                for p in order:
                    d_id=p.dealer_id
                    product_id=p.product_id
                    s=Stock_Product.objects.filter(product_id=product_id).order_by('-id').first()
                    if s:
                        stock.append(s)
                        #print(stock)                      
                d=Dealer.objects.get(id=d_id)
                if d:
                    d=d

        elif "Cancel_order" in request.POST:
            order_master_id=request.POST.get('order_master_id')
            r=OrderMaster.objects.get(id=order_master_id)
            r.status='Cancel'
            #r.save()
            return redirect('/order/pending_order/')
            
        context={
            'e':e,
            'o':order,
            'd':d,
            'total':total,
            'stock':stock,
            'oms':oms
        }
        return render(request,'order/cancel_view_order.html',context=context)        
    else:
        return redirect('login')
    

