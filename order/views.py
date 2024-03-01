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
        return render(request,'office/order.html',context=context)
    else:
        return redirect('login')
    


def marketing_dashboard(request):
    if request.session.has_key('marketing_mobile'):
        marketing_mobile = request.session['marketing_mobile']        
        context={}
        stock=[]
        product=[]
        e=Employee.objects.filter(employee_mobile=marketing_mobile).first()
        if e:
            e=Employee.objects.get(employee_mobile=marketing_mobile)
        context={
            'e':e
        }
        return render(request,'office/marketing_dashboard.html',context=context)
    else:
        return redirect('login')
    

