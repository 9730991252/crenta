from django.urls import path
from ajax import views
urlpatterns = [
    path('search_batch_product', views.search_batch_product,name='search_batch_product'),
    path('add_new_batch', views.add_new_batch,name='add_new_batch'),
    path('search_qr_product', views.search_qr_product,name='search_qr_product'),
    path('in_stock', views.in_stock,name='in_stock'),
    path('create_tage', views.create_tage,name='create_tage'),
    ]