from django.urls import path

from . import views

urlpatterns = [
    path("", views.CompanyListView.as_view(), name="company_list"),
    path("company/create", views.CompanyCreateView.as_view(), name="company_create"),
    path("company/<int:pk>", views.CompanyDetailView.as_view(), name="company_detail"),
    path("company/<int:pk>/update", views.CompanyUpdateView.as_view(), name="company_update"),
    path("company/<int:company_pk>/rating_yandex_dynamic", views.CompanyRatingYandexDynamic.as_view(), name="company_rating_yandex_dynamic"),
    path("company/<int:company_pk>/rating_gis_dynamic", views.CompanyRatingGisDynamic.as_view(), name="company_rating_gis_dynamic"),
    path("company/<int:company_pk>/rating_google_dynamic", views.CompanyRatingGoogleDynamic.as_view(), name="company_rating_google_dynamic"),
    path("company/<int:company_pk>/review", views.ReviewListView.as_view(), name="review_list"),
    path("company/<int:company_pk>/review/<int:pk>/update", views.ReviewUpdateView.as_view(), name="review_update"),
    path("company/<int:company_pk>/message", views.MessageListView.as_view(), name="message_list"),
    path("company/<int:company_pk>/qr", views.qr, name="qr"),
    path("company/<int:company_pk>/widget_rating", views.widget_rating, name="widget_rating"),
    path("company/<int:company_pk>/widget_reviews", views.widget_reviews, name="widget_reviews"),
    path("profile", views.profile, name="profile")
]
