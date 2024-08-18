from datetime import date
from store.models import *
from django import template
register = template.Library()

@register.simple_tag
def today_production(id):
    qty = In_item.objects.filter(item_id=id,date__gte=date.today(),date__lte=date.today()).count()
    return qty

@register.inclusion_tag('inclusion_tag/store/today_production_tag.html')
def today_production_tag(id):
    tag = In_item.objects.filter(item_id=id,date__gte=date.today(),date__lte=date.today()).order_by('tag_number')
    return {
        'tag':tag
    } 

@register.simple_tag
def today_production_employee(id):
    qty = In_item.objects.filter(item_id=id,date__gte=date.today(),date__lte=date.today()).count()
    return qty

@register.simple_tag
def today_production_machine(m_id):
    qty = In_item.objects.filter(machine_id=m_id,date__gte=date.today(),date__lte=date.today()).count()
    return qty


@register.inclusion_tag('inclusion_tag/store/today_production_tag.html')
def today_production_in_tag(id):
    tag = In_item.objects.filter(item_id=id,date__gte=date.today(),date__lte=date.today()).order_by('tag_number')
    return {
        'tag':tag
    } 

@register.simple_tag
def out_item_total(v_id,i_id):
    return Out_item.objects.filter(voucher_id=v_id,item_id=i_id).count()


@register.inclusion_tag('inclusion_tag/store/out_tag_list.html')
def out_tag_list(v_id,i_id):
    tag = Out_item.objects.filter(voucher_id=v_id,item_id=i_id).order_by('tag_number')
    return {
        'tag':tag
    } 