from django import template
from order.models import *
from qr_code.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
from datetime import date
register = template.Library()

@register.simple_tag
def today_production(id):
    qty = In_stock.objects.filter(product_id=id,date__gte=date.today(),date__lte=date.today()).count()
    return qty