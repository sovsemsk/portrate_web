from django.urls import path

from . import views

urlpatterns = [
    path("<str:company_api_secret>/javascript.js", views.javascript, name="widget_javascript"),
    path("<str:company_api_secret>/rate", views.rate, name="widget_rate"),
]

