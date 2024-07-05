from django import template
from order.models import *
from qr_code.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
from datetime import date
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def today_production(id):
    qty = In_stock.objects.filter(product_id=id,date__gte=date.today(),date__lte=date.today()).count()
    return qty


@register.simple_tag
def out_voucher_qty(id,v_id):
    qty = Out_stock.objects.filter(product_id=id,voucher_id=v_id).count()
    return qty


@register.simple_tag
def total_stock_qty(id):
    qty = Qr_code.objects.filter(product_id=id,in_status=1,out_status=0).count()
    #qty = In_stock.objects.filter(product_id=id,status=1).count()
    return qty


@register.simple_tag
def used_tag_emp(tag):
    eid = ''
    emp = In_stock.objects.filter(tag_number=tag).first()
    if emp:
        eid =emp.employee.employee_name
    return eid

@register.simple_tag
def out_tag_emp(tag):
    eid = ''
    emp = Out_stock.objects.filter(tag_number=tag).first()
    if emp:
        eid =emp.employee.employee_name
    return eid



@register.simple_tag
def production_date(tag):
    i = In_stock.objects.get(tag_number=tag)
    fromdate = i.date
    todate = date.today()
    day = todate - fromdate 
    return day.days

