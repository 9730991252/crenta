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
    employee_mobile=models.IntegerField(default=True,unique=True)
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

class Dealer(models.Model):
    dealer_shope_name = models.CharField(max_length=100)
    dealer_name = models.CharField(max_length=100)
    dealer_mobile = models.IntegerField(null=True,blank=True)
    dealer_address = models.CharField(max_length=100)
    location = models.CharField(max_length=100,null=True,blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    date=models.DateField(auto_now_add=True,null=True)
    status = models.IntegerField(default=1)

class Add_Product(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT,default=True)
    type = models.CharField(max_length=100,null=True,blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,default=True,null=True)
    qty = models.IntegerField(default=0)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    date=models.DateField(auto_now_add=True,null=True)
    
    def save(self, *args,**kwargs):
        super(Add_Product,self).save(*args,**kwargs)

        stock=Stock_Product.objects.filter(product=self.product).order_by('-id').first()
        if stock:
            q=stock.stock_qty
            z=self.qty
            z=int(z)
            stock_qty = q+z
            
        else:
            stock_qty=self.qty

        Stock_Product.objects.create(
            product=self.product,
            employee=self.employee,
            add_qty=self.qty,
            stock_qty=stock_qty,
            type=self.type

        )




class Sell_Product(models.Model):
    dealer = models.ForeignKey(Dealer,on_delete=models.PROTECT,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,default=True)
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,default=True,null=True)
    qty = models.IntegerField(default=0)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    date=models.DateField(auto_now_add=True,null=True)
    
    def save(self, *args,**kwargs):
        super(Sell_Product,self).save(*args,**kwargs)

        stock=Stock_Product.objects.filter(product=self.product).order_by('-id').first()
        if stock:
            q=stock.stock_qty
            z=self.qty
            z=int(z)
            stock_qty = q-z
            
        else:
            stock_qty=self.qty

        Stock_Product.objects.create(
            product=self.product,
            employee=self.employee,
            sell_qty=self.qty,
            stock_qty=stock_qty


        )



class Stock_Product(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT,default=True)
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,default=True,null=True)
    add_qty = models.IntegerField(default=0)
    sell_qty = models.IntegerField(default=0)
    stock_qty = models.IntegerField(default=0)
    type = models.CharField(max_length=100,null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True,null=True)
    date=models.DateField(auto_now_add=True,null=True)




