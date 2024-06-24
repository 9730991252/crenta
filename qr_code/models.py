from django.db import models
from office.models import *
# Create your models here.
class Qr_code(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT,default=True)
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,default=True,null=True)
    batch = models.ForeignKey(Batch,on_delete=models.PROTECT,default=True,null=True)
    tag_number = models.IntegerField(unique=True)
    sr_num = models.IntegerField()
    in_status = models.IntegerField(default=0)
    out_status = models.IntegerField(default=0)
    generate_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

class Voucher_num(models.Model):
    creted_by = models.ForeignKey(Employee,on_delete=models.PROTECT,default=True,null=True)
    name = models.CharField(max_length=200)


INSTOCK_CHOICE=(
    ('1','Production'),
    ('2','Return'),
)

class In_stock(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,default=True,null=True)
    qr_code = models.ForeignKey(Qr_code,on_delete=models.PROTECT,default=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,default=True)
    tag_number = models.IntegerField(unique=True ,null=True)
    status = models.CharField(choices=INSTOCK_CHOICE,max_length=50)
    generate_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)