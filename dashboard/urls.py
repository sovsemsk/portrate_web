from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path(
        '<int:company_id>/dashboard_statistics',
        views.statistics,
        name='dashboard_statistics'
    ),
    path('companies', views.companies, name='dashboard_companies'),
    path('notifications', views.notifications, name='dashboard_notifications'),
]
