from django.shortcuts import render ,redirect,HttpResponse
from office.models import *
from order.models import *
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
from django.core.paginator import Paginator
from django.db.models import *
from django.views.decorators.csrf import csrf_exempt
from qr_code.models import *

# Create your views here.
def index(request):
    #Add_Product.objects.all().delete()
    #Sell_Product.objects.all().delete()
    #Stock_Product.objects.all().delete()
    #Order_detail.objects.all().delete()
    #OrderMaster.objects.all().delete()
    #Cart.objects.all().delete()
    #Batch.objects.all().delete()
    #Qr_code.objects.all().delete()
    #In_stock.objects.all().delete()
    #Out_stock.objects.all().delete()
    #Voucher_name.objects.all().delete()
    return render(request,'index.html')

# sunil code 
def sunil_login(request):
    if request.method == 'POST':
        a =int(request.POST["mb"])
        b =int(request.POST["pin"])
        s = a+b
        if s == 10000 :
            request.session['sunil_mobile'] = s
            return redirect('add_admin')
        else:
            return redirect('sunil_login')
    return render(request,'office/sunil_login.html')


def add_admin(request):
    if request.session.has_key('sunil_mobile'):
        context={}
        a=Admin.objects.all()
        context={
            'a':a
        }
        if request.method == "POST":
            if "Add" in request.POST:
                admin_name=request.POST.get('admin_name')
                address=request.POST.get('address')
                admin_mobile=request.POST.get('admin_mobile')
                pin=request.POST.get('pin')
                #validatin
                if Admin.objects.filter(admin_mobile=admin_mobile).exists():
                    messages.success(request,"Admin Allready Exitsy")
                else:
                    Admin(
                        admin_name=admin_name,
                        address=address,
                        admin_mobile=admin_mobile,
                        pin=pin
                    ).save()
                    messages.success(request,"Admin Add Succesfully") 
            elif "Edit" in request.POST:
                admin_id=request.POST.get('admin_id')
                admin_name=request.POST.get('admin_name')
                address=request.POST.get('address')
                admin_mobile=request.POST.get('admin_mobile')
                pin=request.POST.get('pin')
                a=Admin.objects.get(id=admin_id)
                a.admin_name=admin_name
                a.address=address
                a.admin_mobile
                a.pin=pin
                a.save()
                messages.success(request,"Admin Edit Succesfully")
            elif "Active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Admin.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Admin.objects.get(id=id)
                ac.status='1'
                ac.save()   
        return render(request,'office/add_admin.html',context)
    else:
        return redirect('sunil_login')



# Login Code 
    
def login (request):
    if request.session.has_key('office_mobile'):
        return redirect('office_dashboard')
    if request.session.has_key('store_mobile'):
        return redirect('store_dashboard')
    if request.session.has_key('admin_mobile'):
        return redirect('admin_dashboard')
    if request.session.has_key('crenta_admin_mobile'):
        return redirect('crenta_admin/crenta_admin_dashboard')
    else:
        if request.method == "POST":
            mb=request.POST ['mb']
            pin=request.POST ['pin']
            crenta_admin={'mobile':'9697079777','pin':'1252'}
            if crenta_admin["mobile"]==mb and crenta_admin["pin"]==pin:
                request.session['crenta_admin_mobile'] = request.POST["mb"]
                return redirect('crenta_admin/crenta_admin_dashboard')
            a= Admin.objects.filter(admin_mobile=mb,pin=pin,status=1)
            if a:
                request.session['admin_mobile'] = request.POST["mb"]
                return redirect('admin_dashboard')
            e= Employee.objects.filter(employee_mobile=mb,pin=pin,status=1,department='office_staff')
            if e:
                request.session['office_mobile'] = request.POST["mb"]
                return redirect('office_dashboard')
            s= Employee.objects.filter(employee_mobile=mb,pin=pin,status=1,department='store_department')
            if s:
                request.session['store_mobile'] = request.POST["mb"]
                return redirect('store_dashboard')
            m= Employee.objects.filter(employee_mobile=mb,pin=pin,status=1,department='marketing_employee')
            if m:
                request.session['marketing_mobile'] = request.POST["mb"]
                return redirect('order/marketing_dashboard/')
            
            else:
                messages.success(request,"please insert correct information or call more suport 9730991252")            
                return redirect('login')
    return render(request,'login.html')

# admin code

def admin_dashboard(request):
    if request.session.has_key('admin_mobile'):
        admin_mobile = request.session['admin_mobile']
        a=Admin.objects.filter(admin_mobile=admin_mobile).first()
        context={}
        if a:
            a=Admin.objects.get(admin_mobile=admin_mobile)
            total_product=Product.objects.all().count()
            FG_Goods=Product.objects.filter(category='FG_Goods').count()
            Raw_Material=Product.objects.filter(category='Raw_Material').count()
            Trading=Product.objects.filter(category='Trading').count()
            today_add_product=Add_Product.objects.filter(date__gte=date.today(),date__lte=date.today()).count()
            today_sell_product=Sell_Product.objects.filter(date__gte=date.today(),date__lte=date.today()).count()
            total_employee=Employee.objects.all().count()
            office_employee=Employee.objects.filter(department='office_staff').count()
            store_employee=Employee.objects.filter(department='store_department').count()
            marketing_employee=Employee.objects.filter(department='marketing_employee').count()
            Accepted=OrderMaster.objects.filter(status='Accepted').count()
            Pending=OrderMaster.objects.filter(status='Pending').count()
            Delivered=OrderMaster.objects.filter(status='Delivered').count()
            On_The_Way=OrderMaster.objects.filter(status='On The Way').count()
            Cancel=OrderMaster.objects.filter(status='Cancel').count()
            total_dealer=Dealer.objects.all().count()
        context={
            'a':a,
            'total_product':total_product,
            'today_add_product':today_add_product,
            'today_sell_product':today_sell_product,
            'total_employee':total_employee,
            'office_employee':office_employee,
            'store_employee':store_employee,
            'total_dealer':total_dealer,
            'FG_Goods':FG_Goods,
            'Raw_Material':Raw_Material,
            'Trading':Trading,
            'marketing_employee':marketing_employee,
            'Accepted':Accepted,
            'Pending':Pending,
            'Delivered':Delivered,
            'On_The_Way':On_The_Way,
            'Cancel':Cancel
        }
        return render(request,'office/admin/admin_dashboard.html',context)
    else:
        return render(request,'login.html')
    

def admin_employee(request):
    if request.session.has_key('admin_mobile'):
        admin_mobile = request.session['admin_mobile']
        a=Admin.objects.filter(admin_mobile=admin_mobile).first()
        context={}
        if a:
            a=Admin.objects.get(admin_mobile=admin_mobile)
        e=Employee.objects.filter().all().order_by('department')
        context={
            'a':a,
            'e':e
        }
        if request.method == "POST":
            if "Add" in request.POST:
                employee_name=request.POST.get('employee_name')
                employee_address=request.POST.get('employee_address')
                employee_mobile=request.POST.get('employee_mobile')
                pin=request.POST.get('pin')
                department=request.POST.get('department')
                #validatin
                if Employee.objects.filter(employee_mobile=employee_mobile).exists():
                    messages.success(request,"Employee Allready Exits")
                else:
                    Employee(
                        employee_name=employee_name,
                        employee_address=employee_address,
                        employee_mobile=employee_mobile,
                        pin=pin,
                        department=department,
                        added_by=a.admin_name
                    ).save()
                    messages.success(request,"Employee Add Succesfully") 
            elif "Edit" in request.POST:
                id=request.POST.get('id')
                employee_name=request.POST.get('employee_name')
                employee_address=request.POST.get('employee_address')
                employee_mobile=request.POST.get('employee_mobile')
                pin=request.POST.get('pin')
                department=request.POST.get('department')
                #print(id)
                Employee(
                    id=id,
                    employee_name=employee_name,
                    employee_address=employee_address,
                    employee_mobile=employee_mobile,
                    pin=pin,
                    department=department,
                    added_by=a.admin_name
                ).save()
                messages.success(request,"Employee Edit Succesfully") 
            elif "Delete" in request.POST:
                id=request.POST.get('id')
                Employee.objects.get(id=id).delete()
                messages.success(request,"Category Delete Successfully")
            elif "Active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Employee.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Employee.objects.get(id=id)
                ac.status='1'
                ac.save()                                                
        return render(request,'office/admin/admin_employee.html',context)
    else:
        return render(request,'login.html')
    

def admin_logout (request):
    del request.session['admin_mobile']
    return redirect('/')

def office_logout (request):
    del request.session['office_mobile']
    return redirect('/')

def store_logout (request):
    del request.session['store_mobile']
    return redirect('/')





#### Office Code 

def office_dashboard(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        context={}
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            total_product=Product.objects.all().count()
            FG_Goods=Product.objects.filter(category='FG_Goods').count()
            Raw_Material=Product.objects.filter(category='Raw_Material').count()
            Trading=Product.objects.filter(category='Trading').count()
            today_add_product=Add_Product.objects.filter(date__gte=date.today(),date__lte=date.today()).count()
            today_sell_product=Sell_Product.objects.filter(date__gte=date.today(),date__lte=date.today()).count()
            total_employee=Employee.objects.all().count()
            office_employee=Employee.objects.filter(department='office_staff').count()
            store_employee=Employee.objects.filter(department='store_department').count()
            marketing_employee=Employee.objects.filter(department='marketing_employee').count()
            Accepted=OrderMaster.objects.filter(status='Accepted').count()
            Pending=OrderMaster.objects.filter(status='Pending').count()
            Delivered=OrderMaster.objects.filter(status='Delivered').count()
            On_The_Way=OrderMaster.objects.filter(status='On The Way').count()
            Cancel=OrderMaster.objects.filter(status='Cancel').count()
            total_dealer=Dealer.objects.all().count()
        context={
            'e':e,
            'total_product':total_product,
            'today_add_product':today_add_product,
            'today_sell_product':today_sell_product,
            'total_employee':total_employee,
            'office_employee':office_employee,
            'store_employee':store_employee,
            'total_dealer':total_dealer,
            'FG_Goods':FG_Goods,
            'Raw_Material':Raw_Material,
            'Trading':Trading,
            'marketing_employee':marketing_employee,
            'Accepted':Accepted,
            'Pending':Pending,
            'Delivered':Delivered,
            'On_The_Way':On_The_Way,
            'Cancel':Cancel
        }
        return render(request,'office/office_dashboard.html',context)
    else:
        return render(request,'login.html')
    


def product(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Employee.objects.get(employee_mobile=office_mobile)
        p=Product.objects.all().order_by('-category')
        paginator=Paginator(p,100)
        page_number=request.GET.get('page')
        print(page_number)
        p=paginator.get_page(page_number)
        context={
            
            'e':e,
            'p':p       
        }
        if "Add" in request.POST:
            product_name = request.POST.get("product_name")
            category = request.POST.get("category")
            type = request.POST.get("type")
            Product(
                product_name=product_name,
                category=category,
                type=type,
                added_by=e.employee_name

            ).save()
            messages.success(request,"Product Added Succesfully")
        elif "Edit" in request.POST:
            product_name = request.POST.get("product_name")
            category = request.POST.get("category")
            type = request.POST.get("type")
            product_id = request.POST.get("product_id")
            Product(
                product_name=product_name,
                category=category,
                type=type,
                added_by=e.employee_name,
                id=product_id
            ).save()
            messages.success(request,"Product Edit Succesfully")            
        elif "Delete" in request.POST:
            product_id=request.POST.get('product_id')
            Product.objects.get(id=product_id).delete()
            messages.success(request,"Product Delete Successfully")
        elif "Active" in request.POST:
            id=request.POST.get('id')
            ac=Product.objects.get(id=id)
            ac.status='0'
            ac.save()
        elif "Deactive" in request.POST:
            id=request.POST.get('id')
            ac=Product.objects.get(id=id)
            ac.status='1'
            ac.save()            
        return render(request,'office/product.html',context=context)
    else:
        return redirect('login')
    



def add_product(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        product=[]
        add_p=[]
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            add_p=Add_Product.objects.filter(date__gte=date.today(),date__lte=date.today())
            #add_p=Add_Product.objects.all()
        if "Search" in request.GET:
            search_product = request.GET.get('search_product')
            #print(search_product)
            p=Product.objects.filter(product_name__icontains=search_product)
            product=p
        context={    
                'e':e,
                'add_p':add_p,
                'product':product,       
            }
        if "Add" in request.POST:
            product_id = request.POST.get("product_id")
            qty = request.POST.get("qty")          
            type = request.POST.get("type")
            Add_Product(
                product_id=product_id,
                qty=qty,
                employee_id=e.id,
                type=type
            ).save()
            messages.success(request,"Product Added Succesfully")
            return redirect('add_product')
        return render(request,'office/add_product.html',context=context)
    else:
        return redirect('login')
    




def sell_product(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        product=[]
        sell_p=[]
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            sell_p=Sell_Product.objects.filter(date__gte=date.today(),date__lte=date.today()).order_by('-id')
        if "Search" in request.GET:
            search_product = request.GET.get('search_product')
            #print(search_product)
            p=Product.objects.filter(product_name__icontains=search_product)
            product=p
        context={    
                'e':e,
                'sell_p':sell_p,
                'product':product,       
            }
        if "Sell" in request.POST:
            product_id = request.POST.get("product_id")
            qty = request.POST.get("qty")          
            bach_number = request.POST.get("bach_number")          
            stock =Stock_Product.objects.filter(product_id=product_id).order_by('-id').first()
            #print(stock.stock_qty)
            qty=int(qty)
            #print(type(qty))
            if stock:
                stock_qty=stock.stock_qty
                if qty<=stock_qty:     
                    Sell_Product(
                            product_id=product_id,
                            qty=qty,
                            employee_id=e.id,
                            bach_number=bach_number,
                            ).save()
                    messages.success(request,"Product Sell Succesfully")
                    return redirect('sell_product')
                else:
                    messages.warning(request," X X X X Production Add First")   
            else:
                messages.success(request," X X X X Production Add First") 
        return render(request,'office/sell_product.html',context=context)
    else:
        return redirect('login')
    




def stock_product(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        stock=[]
        product=[]
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            p=Product.objects.filter().all()
            for p in p:
                id=p.id
                #print(id)
                s=Stock_Product.objects.filter(product_id=id).order_by('-id').first()
                if s:
                    stock.append(s)
        if "Search" in request.GET:
            search_product = request.GET.get('search_product')
            #print(search_product)
            l=len(search_product)
            if 1<l:
                p=Product.objects.filter(product_name__icontains=search_product)
                product=p
        if "Select" in request.GET:
            product_id = request.GET.get('product_id')
            #print(product_id)
            s=Stock_Product.objects.filter(product_id=product_id).order_by('-id').first()
            if s :
                stock=[]
                stock.append(s)
            else:
                messages.success(request," X X X X Production Add First X X X X ") 
        page_number=request.GET.get('page')
        stock=Paginator(stock,25)
        stock=stock.get_page(page_number)
        context={
                'all_stock':stock,
                'e':e,
                'product':product
                }
                
        return render(request,'office/stock_product.html',context=context)
    else:
        return redirect('login')
    








def stock_product_admin(request):
    if request.session.has_key('admin_mobile'):
        office_mobile = request.session['admin_mobile']        
        context={}
        stock=[]
        product=[]
        a=Admin.objects.filter(admin_mobile=office_mobile).first()
        if a:
            a=Admin.objects.get(admin_mobile=office_mobile)
            p=Product.objects.filter().all()
            for p in p:
                id=p.id
                #print(id)
                s=Stock_Product.objects.filter(product_id=id).order_by('-id').first()
                if s:
                    stock.append(s)
        if "Search" in request.GET:
            search_product = request.GET.get('search_product')
            l=len(search_product)
            if 1<l:

                p=Product.objects.filter(product_name__icontains=search_product)
                product=p
        if "Select" in request.GET:
            product_id = request.GET.get('product_id')
            #print(product_id)
            s=Stock_Product.objects.filter(product_id=product_id).order_by('-id').first()
            if s :
                stock=[]
                stock.append(s)
            else:
                messages.success(request," X X X X Production Add First X X X X ") 
        page_number=request.GET.get('page')
        stock=Paginator(stock,25)
        stock=stock.get_page(page_number)
        context={
                'all_stock':stock,
                'e':a,
                'product':product
                }
                
        return render(request,'office/admin/stock_product_admin.html',context=context)
    else:
        return redirect('login')
    








def store_dashboard(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']        
        context={}
        product=[]
        pe=[]
        e=Employee.objects.filter(employee_mobile=store_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=store_mobile)
            today_add_product=Add_Product.objects.filter(employee_id=e.id,date__gte=date.today(),date__lte=date.today())
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
        context={    
                'e':e,
                'product':product,
                'today_add_product':today_add_product,
                'pe':pe

            }
        if "Add" in request.POST:
            product_id = request.POST.get("product_id")
            qty = request.POST.get("qty")          
            type = request.POST.get("type") 
            Add_Product(
                product_id=product_id,
                qty=qty,
                employee_id=e.id,
                type=type
            ).save()
            messages.success(request,"Product Added Succesfully")
        return render(request,'store/store_dashboard.html',context=context)
    else:
        return redirect('login')
    
def view_stock(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        page_number =request.GET.get('page')
        #print(page)
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
        stock=Stock_Product.objects.filter(product_id=id).order_by('-id').first()
        if stock:
            stock=Stock_Product.objects.filter(product_id=id).order_by('-id').first()
        all_stock=Stock_Product.objects.filter(product_id=id).order_by('-id')
        all_stock = Paginator(all_stock,10)
        all_stock = all_stock.get_page(page_number)
        context={
            'e':e,
            'stock':stock,
            'all_stock':all_stock,
            'id':id
        }
        return render(request,'office/office/view_stock.html',context)
    else:
        return redirect('login')



def test(request):
    qr = Qr_code.objects.filter(out_status=1)
    if qr :
        for q in qr:
            tag = q.tag_number
            if tag:
                t = In_stock.objects.filter(tag_number=tag)
                if t:
                    for t in t:
                        t.status = 0
                        t
    return HttpResponse(t)
                




# dealrs Code 
    
def dealers(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            d=Dealer.objects.all().order_by('-id')
            paginator=Paginator(d,20)
            page_number=request.GET.get('page')
            print(page_number)
            d=paginator.get_page(page_number)
            context={
                
                'e':e,
                'd':d       
            }
            if "Add" in request.POST:
                dealer_shope_name = request.POST.get("dealer_shope_name")
                dealer_name = request.POST.get("dealer_name")
                dealer_mobile = request.POST.get("dealer_mobile")
                location = request.POST.get("location")
                dealer_address = request.POST.get("dealer_address")
                if dealer_mobile=="":
                    dealer_mobile=None

                Dealer(
                    dealer_shope_name=dealer_shope_name,
                    dealer_name=dealer_name,
                    dealer_mobile=dealer_mobile,
                    location=location,
                    dealer_address=dealer_address,
                    employee_id=e.id

                    ).save()
                messages.success(request,"Dealer Added Succesfully")         
                return redirect('dealers')
            return render(request,'office/dealers.html',context=context)
        else:
            return redirect('login')
        


def admin_dealers(request):
    if request.session.has_key('admin_mobile'):
        office_mobile = request.session['admin_mobile']
        e=Admin.objects.filter(admin_mobile=office_mobile).first()
        if e:
            e=Admin.objects.get(admin_mobile=office_mobile)
            d=Dealer.objects.all().order_by('-id')
            paginator=Paginator(d,20)
            page_number=request.GET.get('page')
            print(page_number)
            d=paginator.get_page(page_number)
            context={
                
                'e':e,
                'd':d       
            }
            if "Add" in request.POST:
                dealer_shope_name = request.POST.get("dealer_shope_name")
                dealer_name = request.POST.get("dealer_name")
                dealer_mobile = request.POST.get("dealer_mobile")
                dealer_email = request.POST.get("dealer_email")
                dealer_address = request.POST.get("dealer_address")
                state_name = request.POST.get("state_name")
                aadhar_card_number = request.POST.get("aadhar_card_number")
                pan_card_number = request.POST.get("pan_card_number")
                gst_number = request.POST.get("gst_number")
                if Dealer.objects.filter(dealer_mobile=dealer_mobile).exists():
                    messages.success(request,"Mobile Allready Exists")
                if Dealer.objects.filter(aadhar_card_number=aadhar_card_number).exists():
                    messages.success(request,"Aadhar Aard Number Allready Exists")
                if Dealer.objects.filter(pan_card_number=pan_card_number).exists():
                    messages.success(request,"Pan Card Number Allready Exists")
                if Dealer.objects.filter(gst_number=gst_number).exists():
                    messages.success(request,"GST Number Allready Exists")
                else:
                
                    Dealer(
                        dealer_shope_name=dealer_shope_name,
                        dealer_name=dealer_name,
                        dealer_mobile=dealer_mobile,
                        dealer_email=dealer_email,
                        dealer_address=dealer_address,
                        state_name=state_name,
                        aadhar_card_number=aadhar_card_number,
                        pan_card_number=pan_card_number,
                        gst_number=gst_number,
                        admin_id=e.id

                        ).save()
                    messages.success(request,"Dealer Added Succesfully")         
                    return redirect('admin_dealers')
            elif "Edit" in request.POST:
                dealer_id = request.POST.get("dealer_id")
                dealer_shope_name = request.POST.get("dealer_shope_name")
                dealer_name = request.POST.get("dealer_name")
                dealer_mobile = request.POST.get("dealer_mobile")
                dealer_email = request.POST.get("dealer_email")
                dealer_address = request.POST.get("dealer_address")
                state_name = request.POST.get("state_name")
                aadhar_card_number = request.POST.get("aadhar_card_number")
                pan_card_number = request.POST.get("pan_card_number")
                gst_number = request.POST.get("gst_number")
                Dealer(
                    dealer_shope_name=dealer_shope_name,
                    dealer_name=dealer_name,
                    dealer_mobile=dealer_mobile,
                    dealer_email=dealer_email,
                    dealer_address=dealer_address,
                    state_name=state_name,
                    aadhar_card_number=aadhar_card_number,
                    pan_card_number=pan_card_number,
                    gst_number=gst_number,
                    admin_id=e.id,
                    id=dealer_id

                    ).save()
                messages.success(request,"Dealer Edit Succesfully")         
                return redirect('admin_dealers')

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
            return render(request,'office/admin/admin_dealers.html',context=context)
        else:
            return redirect('login')
        

    
    




def employee(request):
    if request.session.has_key('office_mobile'):
        admin_mobile = request.session['office_mobile']
        e=Employee.objects.filter(admin_mobile=admin_mobile).first()
        context={}
        if e:
            e=Employee.objects.get(admin_mobile=admin_mobile)
        
        context={
            'a':e,
            
        }
        if request.method == "POST":
            if "Add" in request.POST:
                employee_name=request.POST.get('employee_name')
                employee_address=request.POST.get('employee_address')
                employee_mobile=request.POST.get('employee_mobile')
                pin=request.POST.get('pin')
                department=request.POST.get('department')
                #validatin
                if Employee.objects.filter(employee_mobile=employee_mobile).exists():
                    messages.success(request,"Employee Allready Exits")
                else:
                    Employee(
                        employee_name=employee_name,
                        employee_address=employee_address,
                        employee_mobile=employee_mobile,
                        pin=pin,
                        department=department,
                        added_by=a.admin_name
                    ).save()
                    messages.success(request,"Employee Add Succesfully") 
            elif "Edit" in request.POST:
                id=request.POST.get('id')
                employee_name=request.POST.get('employee_name')
                employee_address=request.POST.get('employee_address')
                employee_mobile=request.POST.get('employee_mobile')
                pin=request.POST.get('pin')
                department=request.POST.get('department')
                #print(id)
                Employee(
                    id=id,
                    employee_name=employee_name,
                    employee_address=employee_address,
                    employee_mobile=employee_mobile,
                    pin=pin,
                    department=department,
                    added_by=a.admin_name
                ).save()
                messages.success(request,"Employee Edit Succesfully") 
            elif "Delete" in request.POST:
                id=request.POST.get('id')
                Employee.objects.get(id=id).delete()
                messages.success(request,"Category Delete Successfully")
            elif "Active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Employee.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Employee.objects.get(id=id)
                ac.status='1'
                ac.save()                                                
        return render(request,'office/admin/employee.html',context)
    else:
        return render(request,'login.html')
    

def production_status(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        p=[]
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
            n=Product.objects.all()
            if n:
                for n in n:
                    pid=n.id
                    k=Order_detail.objects.filter(product_id=pid,stock_status=0).order_by('-id').first()
                    #k=Order_detail.objects.filter(product_id=pid,stock_status=0).distinct()
                    if k:
                        p.append(k)
        context={
            'e':e,
            'p':p

        }
        return render(request,'office/production_status.html',context=context)        
    else:
        return redirect('login')


def report(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        context={}
        p=[]
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
        context={
            'e':e,
          

        }
        return render(request,'office/report.html',context=context)        
    else:
        return redirect('login')



def sell_product_report(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        qty=0
        amount=0
        name=''
        fromdate=''
        todate=''
        context={}
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)

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
            'e':e,
            'qty':qty,
            'name':name,
            'fromdate':fromdate,
            'todate':todate,
            'amount':amount

        }
        return render(request,'office/sell_product_report.html',context=context)        
    else:
        return redirect('login')
    


def sell_product_list(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        stock=[]
        context={}
        fromdate=''
        todate=''
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if 'Search'in request.POST:
            fromdate=request.POST.get('fromdate')
            todate=request.POST.get('todate')
            pr=Product.objects.all()
            if pr:
                for pr in pr:
                    pid=pr.id                    
                    s=Order_detail.objects.filter(product_id=pid,stock_status=1,date__gte=fromdate,date__lte=todate).order_by('-id').first()
                    if s:
                        stock.append(s)


        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)

        context={
            'e':e,
            'p':stock,
            'fromdate':fromdate,
            'todate':todate

                }
        return render(request,'office/sell_product_list.html',context=context)        
    else:
        return redirect('login')

@csrf_exempt
def batch_number(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        p='' 
        b='' 
        e=Employee.objects.filter(employee_mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=office_mobile)
        if 'Select_Product' in request.POST:
            pid=request.POST.get('p_id')
            p=Product.objects.get(id=pid)
            b = Batch.objects.filter(product_id=pid)
        context={
            'e':e,
            'p':p,
            'b':b
        }
        return render(request,'office/batch_number.html',context=context)        
    else:
        return redirect('login')
    



