from django.urls import path
from office import views

urlpatterns = [
    path('office_home/', views.office_home , name='office_home'),
    path('employee/', views.employee , name='employee'),
    path('item/', views.item, name='item'),
    path('office_employee/', views.office_employee , name='office_employee'),
    path('store_employee/', views.store_employee , name='store_employee'),
    path('generate_qr_code/', views.generate_qr_code , name='generate_qr_code'),
    path('verify_qr_code', views.verify_qr_code,name='verify_qr_code'),
    path('pending_verify_qr_code', views.pending_verify_qr_code,name='pending_verify_qr_code'),
    path('pending_view_voucher/<int:id>', views.pending_view_voucher,name='pending_view_voucher'),
    path('accepted_verify_qr_code', views.accepted_verify_qr_code,name='accepted_verify_qr_code'),
    path('marketing_employee/', views.marketing_employee,name='marketing_employee'),
    path('dealer/', views.dealer,name='dealer'),
    path('accepted_view_voucher/<int:id>', views.accepted_view_voucher,name='accepted_view_voucher'),
    path('order/', views.order,name='order'),
    path('pending_order/', views.pending_order,name='pending_order'),
    path('accepted_order/', views.accepted_order,name='accepted_order'),
    path('view_pending_order/<marketing_employee_id>/<dealer_id>/', views.view_pending_order,name='view_pending_order'),
    path('view_accepted_order/<id>/', views.view_accepted_order,name='view_accepted_order'),
]