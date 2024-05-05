from django import template
from order.models import *
from django.db.models import Avg, Sum, Min, Max

register = template.Library()

@register.simple_tag
def call_stock(id):
    s=Stock_Product.objects.filter(product_id=id).order_by('-id').first()
    if s == None:
        return 0
    if s:
        return s.stock_qty


@register.simple_tag
def order_qty(id):
    p=Order_detail.objects.filter(product_id=id,stock_status=0)
    #print(p)
    n=0
    if p:
        for p in p:
            qty=p.qty
            n += qty
        return n
    

@register.simple_tag
def pending_order_amount():
    p=Order_detail.objects.filter(stock_status=0)
    #print(p)
    a=0
    if p:
        for p in p:
            total=p.total_price
            a += total
        return a


@register.simple_tag
def accepted_order_amount():
    p=Order_detail.objects.filter(stock_status=1)
    #print(p)
    a=0
    if p:
        for p in p:
            total=p.total_price
            a += total
        return a
    

  
@register.simple_tag
def qty_status(id):
    p=Order_detail.objects.filter(product_id=id,stock_status=0)
    s=Stock_Product.objects.filter(product_id=id).order_by('-id').first()
    if s == None:
        return 0
    
    n=0
    if p:
        for p in p:
            qty=p.qty
            n += qty
            s_q= s.stock_qty - n
        return s_q
    

  
  
@register.simple_tag
def sell_qty(id,fromdate,todate):
    p=Order_detail.objects.filter(product_id=id,stock_status=1,date__gte=fromdate,date__lte=todate)
    n=0
    if p:
        for p in p:
            qty=p.qty
            n += qty
        return n

  
  
@register.simple_tag
def sell_total(id,fromdate,todate):
    p=Order_detail.objects.filter(product_id=id,stock_status=1,date__gte=fromdate,date__lte=todate)
    n=0
    if p:
        for p in p:
            a=p.total_price
            n += a
        return n


@register.simple_tag
def sell_product_total(id):
    p=Order_detail.objects.filter(product_id=id,stock_status=1)
    a=(p.aggregate(a=Sum('price')))
    #print(a['a'])
    return a['a']


@register.simple_tag
def sell_product_average(id):
    p=Order_detail.objects.filter(product_id=id,stock_status=1)
    a=(p.aggregate(a=Avg('price')))
    #print(a['a'])
    return a['a']


@register.simple_tag
def sell_product_max(id):
    p=Order_detail.objects.filter(product_id=id,stock_status=1)
    a=(p.aggregate(a=Max('price')))
    #print(a['a'])
    return a['a']

@register.simple_tag
def sell_product_min(id):
    p=Order_detail.objects.filter(product_id=id,stock_status=1)
    a=(p.aggregate(a=Min('price')))
    #print(a['a'])
    return a['a']
