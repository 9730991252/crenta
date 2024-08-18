from django.urls import path
from sunil import views
urlpatterns = [
    path('add_employee_sunil/', views.add_employee_sunil, name='add_employee_sunil'),
]