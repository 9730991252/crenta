from django.urls import path ,include
from . import views
urlpatterns = [
    path('marketing_home/', views.marketing_home, name='marketing_home'),
    path('order/', views.order, name='order'),
    path('completed_order/', views.completed_order, name='completed_order'),
    path('select_dealer/<id>', views.select_dealer, name='select_dealer'),
    path('complate_view_order/<order_filter>', views.complate_view_order, name='complate_view_order'),
]