from django import template
from order.models import *

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
    p=Order_detail.objects.filter(product_id=id)
    n=0
    if p:
        for p in p:
            qty=p.qty
            n += qty
        return n
    

  
