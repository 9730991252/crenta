from django.urls import path
from qr_code import views
urlpatterns = [
    path('qr_code', views.qr_code,name='qr_code'),
    path('verify_qr_code', views.verify_qr_code,name='verify_qr_code'),
    path('pending_verify_qr_code', views.pending_verify_qr_code,name='pending_verify_qr_code'),
    path('accepted_verify_qr_code', views.accepted_verify_qr_code,name='accepted_verify_qr_code'),
    path('pending_view_voucher/<int:id>', views.pending_view_voucher,name='pending_view_voucher'),
    path('accepted_view_voucher/<int:id>', views.accepted_view_voucher,name='accepted_view_voucher'),
    path('in_product', views.in_product,name='in_product'),
    path('voucher_add_stock/<int:id>', views.voucher_add_stock,name='voucher_add_stock'),
    path('out_product', views.out_product,name='out_product'),
    path('stock_list', views.stock_list,name='stock_list'),
    path('unused_tag_list', views.unused_tag_list,name='unused_tag_list'),
    ]