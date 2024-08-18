from django.db import models

# Create your models here.
class Office_employee(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    status = models.IntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True, null=True)

class Store_employee(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    status = models.IntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True, null=True)


class Item(models.Model):
    name = models.CharField(max_length=100)
    sr_num = models.IntegerField(null=True)
    employee = models.ForeignKey(Office_employee,on_delete=models.PROTECT,null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True,null=True)
    status = models.IntegerField(default=1)

class Batch(models.Model):
    item = models.ForeignKey(Item,on_delete=models.PROTECT,default=True)
    in_employee = models.ForeignKey(Store_employee,on_delete=models.PROTECT,default=True,null=True)
    sr_num = models.IntegerField()
    batch_name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

class Qr_code(models.Model):
    item = models.ForeignKey(Item,on_delete=models.PROTECT,null=True)
    employee = models.ForeignKey(Office_employee,on_delete=models.PROTECT,null=True)
    batch = models.ForeignKey(Batch,on_delete=models.PROTECT,null=True)
    tag_number = models.IntegerField(unique=True)
    in_status = models.IntegerField(default=0)
    out_status = models.IntegerField(default=0)
    generate_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
