from django.shortcuts import render,redirect
from office.models import *
from order.models import *
from datetime import date

# Create your views here.

def crenta_admin_dashboard(request):
    if request.session.has_key('crenta_admin_mobile'):
        pe=[]
        product=[]
        today_add_product=Add_Product.objects.filter(date__gte=date.today(),date__lte=date.today()).count()
        today_sell_product=Sell_Product.objects.filter(date__gte=date.today(),date__lte=date.today()).count()
        Accepted=OrderMaster.objects.filter(status='Accepted').count()
        Pending=OrderMaster.objects.filter(status='Pending').count()
        Delivered=OrderMaster.objects.filter(status='Delivered').count()
        On_The_Way=OrderMaster.objects.filter(status='On The Way').count()
        Cancel=OrderMaster.objects.filter(status='Cancel').count()
        n=Product.objects.all()
        if n:
            for n in n:
                pid=n.id
                k=Order_detail.objects.filter(product_id=pid,stock_status=0).order_by('-id').first()
                if k:
                    pe.append(k)
        if "Search" in request.GET:
            search_product = request.GET.get('search_product')
            l=len(search_product)
            if 1<l:
                p=Product.objects.filter(product_name__icontains=search_product)
            #print(search_product)
                product=p
        context={}
        context={
            'today_add_product':today_add_product,
            'today_sell_product':today_sell_product,
            'Accepted':Accepted,
            'Pending':Pending,
            'Delivered':Delivered,
            'On_The_Way':On_The_Way,
            'Cancel':Cancel,
            'pe':pe  ,
            'product':product
        }
        return render(request,'crenta_admin/crenta_admin_dashboard.html',context)
    else:
        return render(request,'login.html')




def sell_product_report_crenta_admin(request):
    if request.session.has_key('crenta_admin_mobile'):      
        qty=0
        amount=0
        name=''
        fromdate=''
        todate=''
        context={}
        if 'Search'in request.POST:
            p_id=request.POST.get('product_id')
            #print(p_id)
            fromdate=request.POST.get('fromdate')
            todate=request.POST.get('todate')
            p_id=int(p_id)
            if 0 == p_id:
                p=Order_detail.objects.filter(stock_status=1,date__gte=fromdate,date__lte=todate)
                if p:
                    for p in p:
                        q=p.qty
                        name='all'
                        qty+=q
                        a=p.total_price
                        amount+=a                    
            else :
                p=Order_detail.objects.filter(product_id=p_id,stock_status=1,date__gte=fromdate,date__lte=todate)
                if p:
                    for p in p:
                        q=p.qty
                        name=p.product_name
                        qty+=q
                        a=p.total_price
                        amount+=a
            context={
           
            'qty':qty,
            'name':name,
            'fromdate':fromdate,
            'todate':todate,
            'amount':amount

        }
        return render(request,'crenta_admin/sell_product_report_crenta_admin.html',context=context)        
    else:
        return redirect('login')
    
   

def crenta_admin_logout (request):
    del request.session['crenta_admin_mobile']
    return redirect('/')

