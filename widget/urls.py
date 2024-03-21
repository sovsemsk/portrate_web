from django.urls import path

from . import views

urlpatterns = [
    path("<str:company_api_secret>/rate.js", views.rate, name="widget_rate"),
    path("<str:company_api_secret>/reviews.json", views.reviews_json, name="reviews_json"),

    path("reviews/<str:company_api_secret>.js", views.reviews, name="widget_reviews"),
]