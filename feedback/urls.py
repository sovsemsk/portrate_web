from django.urls import path

from . import views

urlpatterns = [
    path('<int:company_pk>', views.rate, name='feedback_rate'),
    path('<int:company_pk>/create', views.create, name='feedback_create'),
    path('<int:company_pk>/request', views.request, name='feedback_request'),
    path('<int:company_pk>/success', views.success, name='feedback_success')
]
