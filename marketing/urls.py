from django.urls import path ,include
from . import views
urlpatterns = [
    path('marketing_home/', views.marketing_home, name='marketing_home'),
    path('select_diller/<id>', views.select_diller, name='select_diller'),
]