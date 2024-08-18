from django.urls import path
from store import views
urlpatterns = [
    path('store_home/', views.store_home,name='store_home'),
    path('search_in_item/', views.search_in_item,name='search_in_item'),
    path('item_in/<int:item_id>', views.item_in,name='item_in'),
    path('add_voucher/', views.add_voucher, name='add_voucher'),
    path('item_out/<int:id>', views.item_out, name='item_out'),
]