from django.urls import path
from qr_code import views
urlpatterns = [
    path('qr_code', views.qr_code,name='qr_code'),
    path('in_product', views.in_product,name='in_product'),
    ]