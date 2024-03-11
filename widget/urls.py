from django.urls import path

from . import views

urlpatterns = [
    path("<str:company_api_secret>/rate.js", views.rate, name="widget_rate"),
    path("<str:company_api_secret>/reviews.js", views.reviews, name="widget_reviews"),
]