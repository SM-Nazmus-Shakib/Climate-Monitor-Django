from django.urls import path
from . import views

app_name = 'farms'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.farm_list, name='farm_list'),
    path('add/', views.farm_create, name='farm_create'),
    path('<int:farm_id>/', views.farm_detail, name='farm_detail'),
    path('<int:farm_id>/edit/', views.farm_edit, name='farm_edit'),
]