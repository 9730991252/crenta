from django.urls import path
from ajax import views
urlpatterns = [
    path('search_batch_product', views.search_batch_product,name='search_batch_product'),
    path('add_new_batch', views.add_new_batch,name='add_new_batch'),
    path('search_qr_product', views.search_qr_product,name='search_qr_product'),
    path('in_stock', views.in_stock,name='in_stock'),
    path('out_stock', views.out_stock,name='out_stock'),
    path('create_tage', views.create_tage,name='create_tage'),
    path('search_product_admin', views.search_product_admin,name='search_product_admin'),
    path('fetch_batch_admin', views.fetch_batch_admin,name='fetch_batch_admin'),
    path('admin_batch_detail', views.admin_batch_detail,name='admin_batch_detail'),
    ]