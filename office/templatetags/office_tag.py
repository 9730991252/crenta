from django import template
from store.models import *
from datetime import timedelta, date
register = template.Library()

@register.simple_tag
def out_voucher_qty(id,v_id):
    qty = Out_item.objects.filter(item_id=id,voucher_id=v_id).count()
    return qty

@register.simple_tag
def all_stock_count(id):
    return In_item.objects.filter(item_id=id,status=1).count()


@register.inclusion_tag('inclusion_tag/office/in_stock_detail.html')
def in_stock_detail(tag):
    ins = In_item.objects.filter(tag_number=tag).first()
    return {
        'ins':ins
    } 


@register.inclusion_tag('inclusion_tag/office/out_stock_detail.html')
def out_stock_detail(tag):
    outs = Out_item.objects.filter(tag_number=tag).first()
    return {
        'outs':outs
    } 

@register.simple_tag
def out_date(tag):
    i = Out_item.objects.get(tag_number=tag)
    fromdate = i.date
    todate = date.today()
    day = todate - fromdate 
    return day.days



@register.inclusion_tag('inclusion_tag/office/out_voucher_detail.html')
def out_voucher_detail(tag):
    outs = Out_item.objects.filter(tag_number=tag).first()
    return {
        'outs':outs
    } 



@register.simple_tag
def production_date(tag):
    i = In_item.objects.get(tag_number=tag)
    fromdate = i.date
    todate = date.today()
    day = todate - fromdate 
    return day.days