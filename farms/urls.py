from django.urls import path
from .views import farm_map, farm_list, farm_detail, add_farm, add_crop


urlpatterns = [
    path('', farm_map, name='map'),
    path('list/', farm_list, name='list'),
    path('<int:pk>/', farm_detail, name='detail'),
    path('add/', add_farm, name='add'),
    path('<int:farm_id>/add-crop/', add_crop, name='add_crop'),
]