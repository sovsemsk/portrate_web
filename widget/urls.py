from django.urls import path

from .views import reviews

urlpatterns = [
    path("reviews/<str:company_api_secret>.js", reviews, name="widget_reviews")
]
