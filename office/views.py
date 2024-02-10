from django.shortcuts import render ,redirect
from office.models import *
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def index(request):
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
    else:
        if request.method == "POST":
            mb=request.POST ['mb']
            pin=request.POST ['pin']
            a= Admin.objects.filter(admin_mobile=mb,pin=pin,status=1)
            if a:
                request.session['admin_mobile'] = request.POST["mb"]
                return redirect('admin_dashboard')
            e= Employee.objects.filter(employee_mobile=mb,pin=pin,status=1)
            if e:
                request.session['office_mobile'] = request.POST["mb"]
                return redirect('office_dashboard')
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
        
        context={
            'a':a
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

        p=Product.objects.filter().all()
        context={
            
            'e':e,
            'p':p       
        }
        if "Add" in request.POST:
            product_name = request.POST.get("product_name")
            paking = request.POST.get("paking")
            price = request.POST.get("price")
            category = request.POST.get("category")
            type = request.POST.get("type")
            gst = request.POST.get("gst")
            hsn_code = request.POST.get("hsn_code")
            
            Product(
                product_name=product_name,
                paking=paking,
                price=price,
                category=category,
                type=type,
                gst=gst,
                hsn_code=hsn_code,
                added_by=e.employee_name

            ).save()
            messages.success(request,"Product Added Succesfully")
        elif "Edit" in request.POST:
            product_name = request.POST.get("product_name")
            paking = request.POST.get("paking")
            price = request.POST.get("price")
            category = request.POST.get("category")
            type = request.POST.get("type")
            gst = request.POST.get("gst")
            hsn_code = request.POST.get("hsn_code")
            product_id = request.POST.get("product_id")
            Product(
                product_name=product_name,
                paking=paking,
                price=price,
                category=category,
                type=type,
                gst=gst,
                hsn_code=hsn_code,
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
    