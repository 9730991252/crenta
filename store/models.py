from django.db import models
from office.models import *
# Create your models here.
class In_item(models.Model):
    store_employee = models.ForeignKey(Store_employee,on_delete=models.PROTECT,default=True,null=True)
    qr_code = models.ForeignKey(Qr_code,on_delete=models.PROTECT,default=True,null=True)
    item = models.ForeignKey(Item,on_delete=models.PROTECT,default=True)
    tag_number = models.IntegerField(unique=True ,null=True)
    status = models.CharField(max_length=100, null=True)
    scan_type = models.CharField(max_length=100, null=True)
    generate_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

class Voucher_name(models.Model):
    store_employee = models.ForeignKey(Store_employee,on_delete=models.PROTECT,default=True,null=True)
    name = models.CharField(max_length=200)
    verify_by = models.ForeignKey(Office_employee,on_delete=models.PROTECT,null=True)
    verify_status = models.IntegerField(null=True,max_length=100)
    verify_date = models.DateTimeField(null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)


class Out_item(models.Model):
    store_employee = models.ForeignKey(Store_employee,on_delete=models.PROTECT,default=True,null=True)
    qr_code = models.ForeignKey(Qr_code,on_delete=models.PROTECT,default=True,null=True)
    item = models.ForeignKey(Item,on_delete=models.PROTECT,default=True)
    voucher = models.ForeignKey(Voucher_name,on_delete=models.PROTECT,default=True)
    tag_number = models.IntegerField(unique=True ,null=True)
    generate_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    verify_status = models.IntegerField(null=True,default=0)
    verify_date = models.DateTimeField(null=True)
    verify_by = models.ForeignKey(Office_employee,on_delete=models.PROTECT,null=True)
    scan_type = models.CharField(max_length=100, null=True)