from django.urls import path
from .views import report_list, report_detail, create_report, verify_report

app_name = 'damage_report'

urlpatterns = [
    path('', report_list, name='list'),
    path('<int:pk>/', report_detail, name='detail'),
    path('create/', create_report, name='create'),
    path('create/<int:farm_id>/', create_report, name='create_for_farm'),
    path('<int:pk>/verify/', verify_report, name='verify'),
]