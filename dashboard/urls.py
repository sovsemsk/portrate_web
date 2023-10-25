from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('branches', views.branches, name='dashboard_branches'),
]
