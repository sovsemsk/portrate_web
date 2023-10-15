from django.urls import path
from . import views

urlpatterns = [
    path('<int:website_id>', views.rate, name='feedback_rate'),
    path('<int:website_id>/create', views.create, name='feedback_create'),
    path('<int:website_id>/request', views.request, name='feedback_request')
]
