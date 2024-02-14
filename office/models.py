from django.db import models

# Create your models here.


class Admin (models.Model):
    admin_name = models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    admin_mobile=models.IntegerField(default=True,unique=True)
    pin = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1)

class Employee (models.Model):
    employee_name = models.CharField(max_length=100)
    employee_address=models.CharField(max_length=100)
    employee_mobile=models.IntegerField(default=True)
    pin = models.IntegerField()
    department=models.CharField(max_length=50,default=True)
    added_by = models.CharField(max_length=50, default=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1)


class Product(models.Model):
    product_name=models.CharField(max_length=100)
    category=models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=100,null=True,blank=True)
    added_by=models.CharField(max_length=100)
    added_date=models.DateTimeField(auto_now_add=True,null=True)
    status = models.IntegerField(default=1)
