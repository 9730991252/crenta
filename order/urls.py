from django.urls import path
from order import views

urlpatterns = [
    path('', views.order,name='order'),
    path('marketing_dashboard/', views.marketing_dashboard,name='marketing_dashboard'),
    path('product_filter', views.product_filter,name='product_filter'),
    path('add_to_cart', views.add_to_cart,name='add_to_cart'),
    path('pending_order/', views.pending_order,name='pending_order'),
    path('accepted_order/', views.accepted_order,name='accepted_order'),
    path('remove_cart_marketing', views.remove_cart_marketing,name='remove_cart_marketing'),
    path('order_master_marketing/', views.order_master_marketing,name='order_master_marketing'),
    path('marketing_add_order/<int:id>/', views.marketing_add_order,name='marketing_add_order'),
    path('pending_view_order/<int:id>/', views.pending_view_order,name='pending_view_order'),
    path('accepted_view_order/<int:id>/', views.accepted_view_order,name='accepted_view_order'),
]