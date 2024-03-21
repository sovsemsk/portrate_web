from django.urls import path

from .views import rating, reviews

urlpatterns = [
    path("rating/<str:company_api_secret>.js", rating, name="widget_rating"),
    path("reviews/<str:company_api_secret>.js", reviews, name="widget_reviews")
]
