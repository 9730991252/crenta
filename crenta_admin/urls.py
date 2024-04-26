from django.urls import path
from crenta_admin import views
urlpatterns = [
    path('crenta_admin_dashboard', views.crenta_admin_dashboard,name='crenta_admin_dashboard'),
    path('sell_product_report_crenta_admin/', views.sell_product_report_crenta_admin,name='sell_product_report_crenta_admin'),
    path('crenta_admin_logout', views.crenta_admin_logout,name='crenta_admin_logout'),
    ]