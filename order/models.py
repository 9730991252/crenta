from django.db import models
from office.models import *
# Create your models here.
STATUS_CHOICES = (
  ('Accepted','Accepted'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Cancel','Cancel'),
  ('Pending','Pending'),

)


INSTOCK_OUTSTOCK_CHOICE=(
    ('1','in stock'),
    ('0','out of stock')
)



class Cart(models.Model):
    dealer = models.ForeignKey(Dealer,on_delete=models.PROTECT,default=True)
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,default=True)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,default=True)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,default=True)
    type = models.CharField(max_length=100,null=True,blank=True)
    qty = models.IntegerField(default=1)
    price=models.FloatField(default=0,null=True)
    total_price=models.FloatField(default=0,null=True)
    def save(self,*args,**kwargs):
        price=int(self.price)
        qty=int(self.qty)
        self.total_price=price*qty
        super(Cart,self).save()




class OrderMaster(models.Model):
    dealer = models.ForeignKey(Dealer,on_delete=models.PROTECT,default=True)
    marketing_employee_id = models.CharField(max_length=100,null=True,blank=True)
    office_employee_id = models.CharField(max_length=100,null=True,blank=True)
    store_employee_id = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(choices=STATUS_CHOICES,default='Pending',max_length=50)
    total_price=models.FloatField(default=0,null=True)
    order_filter=models.IntegerField(default=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    date=models.DateField(auto_now_add=True,null=True)


class Order_detail(models.Model):
    dealer = models.ForeignKey(Dealer,on_delete=models.PROTECT,default=True)
    marketing_employee_id = models.CharField(max_length=100,null=True,blank=True)
    office_employee_id = models.CharField(max_length=100,null=True,blank=True)
    store_employee_id = models.CharField(max_length=100,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,default=True,null=True,blank=True)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,default=True)
    type = models.CharField(max_length=100,null=True,blank=True)
    order_filter = models.IntegerField(default=True)
    stock_status = models.IntegerField(choices=INSTOCK_OUTSTOCK_CHOICE,default=0)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    date=models.DateField(auto_now_add=True,null=True)
    qty = models.IntegerField(default=1)
    price=models.FloatField(default=0,null=True)
    total_price=models.FloatField(default=0,null=True)
    
    def save(self,*args,**kwargs):
        price=int(self.price)
        qty=int(self.qty)
        self.total_price=price*qty
        super(Order_detail,self).save()
