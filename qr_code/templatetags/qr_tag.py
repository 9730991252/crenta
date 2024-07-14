from django import template
from order.models import *
from qr_code.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
from datetime import date
from django.utils.safestring import mark_safe
from django.db.models import Q
from datetime import timedelta, date
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





@register.inclusion_tag('tag/in_stock_detail.html')
def in_stock_detail(tag):
    ins = In_stock.objects.filter(tag_number=tag).first()
    return {
        'ins':ins
    } 






@register.inclusion_tag('tag/out_stock_detail.html')
def out_stock_detail(tag):
    outs = Out_stock.objects.filter(tag_number=tag).first()
    return {
        'outs':outs
    } 




@register.simple_tag
def production_date(tag):
    i = In_stock.objects.get(tag_number=tag)
    fromdate = i.date
    todate = date.today()
    day = todate - fromdate 
    return day.days

@register.simple_tag
def out_date(tag):
    i = Out_stock.objects.get(tag_number=tag)
    fromdate = i.date
    todate = date.today()
    day = todate - fromdate 
    return day.days



@register.simple_tag
def out_voucher(tag):
    i = Out_stock.objects.get(tag_number=tag)
    print(i)
    return i.voucher.name


@register.inclusion_tag('tag/out_voucher_detail.html')
def out_voucher_detail(tag):
    outs = Out_stock.objects.filter(tag_number=tag).first()
    return {
        'outs':outs
    } 

@register.simple_tag
def old_in_stock(d,pid):
    t = In_stock.objects.filter(status=1,date__lte=d,product_id=pid).count()
    return t

#,product_id=pid

@register.simple_tag
def old_out_stock(d,pid):
    t = Out_stock.objects.filter(date__gte=d,date__lte=date.today(),product_id=pid).count()
    return t

#,product_id=pid 






