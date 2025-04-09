from django.urls import path
from ajax import views
urlpatterns = [
    path('generate_tag', views.generate_tag,name='generate_tag'),
    path('set_item_sr_num', views.set_item_sr_num,name='set_item_sr_num'),
    path('search_in_item_ajax', views.search_in_item_ajax,name='search_in_item_ajax'),
    path('search_marketing_item_ajax', views.search_marketing_item_ajax,name='search_marketing_item_ajax'),
    path('in_item', views.in_item,name='in_item'),
    path('in_item_manual', views.in_item_manual,name='in_item_manual'),
    path('search_tag', views.search_tag,name='search_tag'),
    path('out_item', views.out_item,name='out_item'),
    path('search_out_tag', views.search_out_tag,name='search_out_tag'),
    path('out_item_manual', views.out_item_manual,name='out_item_manual'),
    path('search_item', views.search_item,name='search_item'),
    path('fetch_batch', views.fetch_batch,name='fetch_batch'),
    path('batch_detail', views.batch_detail,name='batch_detail'),
]