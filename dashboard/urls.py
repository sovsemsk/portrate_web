from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('companies', views.companies, name='dashboard_companies'),
]
