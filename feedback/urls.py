from django.urls import path
from . import views

urlpatterns = [
    path('<int:company_id>', views.rate, name='feedback_rate'),
    path('<int:company_id>/create', views.create, name='feedback_create'),
    path('<int:company_id>/request', views.request, name='feedback_request')
]
