from django.urls import path
from . import views

app_name = 'farms'

urlpatterns = [
    # Dashboard and main views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.farm_list, name='farm_list'),
    
    # Farm CRUD operations
    path('add/', views.farm_create, name='farm_create'),
    path('<int:farm_id>/', views.farm_detail, name='farm_detail'),
    path('<int:farm_id>/edit/', views.farm_edit, name='farm_edit'),
    path('<int:farm_id>/delete/', views.farm_delete, name='farm_delete'),
    
    # API endpoints
    path('api/weather/', views.weather_api, name='weather_api'),
    path('api/<int:farm_id>/analytics/', views.farm_analytics, name='farm_analytics'),
    path('api/<int:farm_id>/export/', views.export_farm_data, name='export_farm_data'),
]