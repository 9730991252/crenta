from django.urls import path
from crenta_admin import views
urlpatterns = [
    path('crenta_admin_dashboard', views.crenta_admin_dashboard,name='crenta_admin_dashboard'),
    path('crenta_admin_logout', views.crenta_admin_logout,name='crenta_admin_logout'),
    ]