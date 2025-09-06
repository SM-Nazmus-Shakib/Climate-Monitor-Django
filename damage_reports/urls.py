from django.urls import path
from . import views

app_name = 'damage_reports'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('create/', views.report_create, name='report_create'),
    path('<int:report_id>/', views.report_detail, name='report_detail'),
    path('<int:report_id>/edit/', views.report_edit, name='report_edit'),
]