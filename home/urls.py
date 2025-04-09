from django.urls import path ,include
from home import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('marketing_login/', views.marketing_login, name='marketing_login'),
    path('sunil_login/', views.sunil_login, name='sunil_login'),
    path('office_logout/', views.office_logout, name='office_logout'),
    path('store_logout/', views.store_logout, name='store_logout'),
]