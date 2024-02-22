from django.urls import path

from . import views

urlpatterns = [
    path("<str:company_api_secret>/rate", views.rate, name="widget_rate"),
]

