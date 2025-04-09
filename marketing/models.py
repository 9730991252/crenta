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