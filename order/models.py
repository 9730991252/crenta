from django.db import models

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