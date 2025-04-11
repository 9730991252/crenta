from django.db import models
from office.models import *
# Create your models here.
class marketing_Cart(models.Model):
    marketing_employee = models.ForeignKey(Marketing_employee, on_delete=models.CASCADE, null=True, blank=True)
    dealer  = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)


YEAR_IN_SCHOOL_CHOICES = [
    ("Pendding", "Pendding"),
    ("Accepted", "Accepted"),
    ("Cancled", "Cancled"),
    ("Delivered", "Delivered"),
]
  
class Marketing_order_master(models.Model):
    marketing_employee = models.ForeignKey(Marketing_employee, on_delete=models.CASCADE, null=True, blank=True)
    accepted = models.ForeignKey(Office_employee, on_delete=models.CASCADE, null=True, blank=True)
    dealer  = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
    total_price=models.FloatField(default=0,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    date = models.DateField(auto_now_add=True,null=True)
    order_filter=models.IntegerField(default=True)
    status = models.CharField(default='Pendding', max_length=100, null=True)

class Marketing_order_detail(models.Model):
    order_master=models.ForeignKey(Marketing_order_master,on_delete=models.PROTECT,null=True)
    item=models.ForeignKey(Item,on_delete=models.PROTECT,null=True)
    qty = models.IntegerField(default=1)
    price=models.FloatField(default=0,null=True)
    total_price=models.FloatField(default=0,null=True)
    order_filter=models.IntegerField(default=True)
    date = models.DateField(auto_now_add=True,null=True)
    item_name = models.CharField(max_length=100, null=True)
