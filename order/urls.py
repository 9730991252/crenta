from django.urls import path
from order import views

urlpatterns = [
    path('order/', views.order,name='order'),
    path('marketing_dashboard/', views.marketing_dashboard,name='marketing_dashboard'),
]