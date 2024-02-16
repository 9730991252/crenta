from django.urls import path
from office import views

urlpatterns = [
    path('', views.index,name='index'),
    path('sunil_login', views.sunil_login,name='sunil_login'),
    path('add_admin', views.add_admin,name='add_admin'),
    path('login', views.login,name='login'),
    path('admin_dashboard', views.admin_dashboard,name='admin_dashboard'),
    path('admin_employee', views.admin_employee,name='admin_employee'),
    path('admin_logout', views.admin_logout,name='admin_logout'),
    path('office_dashboard', views.office_dashboard,name='office_dashboard'),
    path('office_logout', views.office_logout,name='office_logout'),
    path('product', views.product,name='product'),
    path('add_product', views.add_product,name='add_product'),
    path('sell_product', views.sell_product,name='sell_product'),
    path('stock_product', views.stock_product,name='stock_product'),
    path('store_dashboard', views.store_dashboard,name='store_dashboard'),
]