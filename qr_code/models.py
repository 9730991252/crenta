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