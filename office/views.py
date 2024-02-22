from django.shortcuts import render ,redirect
from office.models import *
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    #Add_Product.objects.all().delete()
    #Stock_Product.objects.all().delete()
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
    else:
        if request.method == "POST":
            mb=request.POST ['mb']
            pin=request.POST ['pin']
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
            today_add_product=Add_Product.objects.filter(date__gte=date.today(),date__lte=date.today()).count()
            today_sell_product=Sell_Product.objects.filter(date__gte=date.today(),date__lte=date.today()).count()
            total_employee=Employee.objects.all().count()
            office_employee=Employee.objects.filter(department='office_staff').count()
            store_employee=Employee.objects.filter(department='store_department').count()
        context={
            'a':a,
            'total_product':total_product,
            'today_add_product':today_add_product,
            'today_sell_product':today_sell_product,
            'total_employee':total_employee,
            'office_employee':office_employee,
            'store_employee':store_employee
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
        
        context={
            
            'e':e
        }

        return render(request,'office/office/office_dashboard.html',context)
    else:
        return render(request,'login.html')
    


def product(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Employee.objects.get(employee_mobile=office_mobile)
        p=Product.objects.all().order_by('-category')
        paginator=Paginator(p,20)
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
        return render(request,'office/office/product.html',context=context)
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
        return render(request,'office/office/add_product.html',context=context)
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
            sell_p=Sell_Product.objects.filter(date__gte=date.today(),date__lte=date.today())
        if "Search" in request.GET:
            search_product = request.GET.get('search_product')
            print(search_product)
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
            Sell_Product(
                product_id=product_id,
                qty=qty,
                employee_id=e.id
            ).save()
            messages.success(request,"Product Added Succesfully")
        return render(request,'office/office/sell_product.html',context=context)
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
            p=Product.objects.filter(product_name__icontains=search_product)
            product=p
        if "Select" in request.GET:
            product_id = request.GET.get('product_id')
            print(product_id)
            s=Stock_Product.objects.filter(product_id=product_id).order_by('-id').first()
            stock=[]
            stock.append(s)
        page_number=request.GET.get('page')
        stock=Paginator(stock,25)
        stock=stock.get_page(page_number)
        context={
                'all_stock':stock,
                'e':e,
                'product':product
                }
                
        return render(request,'office/office/stock_product.html',context=context)
    else:
        return redirect('login')
    



def store_dashboard(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']        
        context={}
        product=[]
        e=Employee.objects.filter(employee_mobile=store_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=store_mobile)
            today_add_product=Add_Product.objects.filter(employee_id=e.id,date__gte=date.today(),date__lte=date.today())
        if "Search" in request.GET:
            search_product = request.GET.get('search_product')
            print(search_product)
            p=Product.objects.filter(product_name__icontains=search_product)
            product=p
        context={    
                'e':e,
                'product':product,
                'today_add_product':today_add_product

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
        return render(request,'office/store/store_dashboard.html',context=context)
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
            p=Product.objects.filter(product_name__icontains=search_product)
            product=p
        if "Select" in request.GET:
            product_id = request.GET.get('product_id')
            print(product_id)
            s=Stock_Product.objects.filter(product_id=product_id).order_by('-id').first()
            stock=[]
            stock.append(s)
        context={
                'all_stock':stock,
                'e':e,
                'product':product
                }
                
        return render(request,'office/office/test.html',context)
    else:
        return redirect('login')


