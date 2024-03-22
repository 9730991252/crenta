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
