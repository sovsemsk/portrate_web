from django.urls import path

from . import views

urlpatterns = [
    path("", views.CompanyListView.as_view(), name="company_list"),
    path("company/create", views.CompanyCreateView.as_view(), name="company_create"),
    path("company/<int:pk>", views.CompanyDetailView.as_view(), name="company_detail"),
    path("company/<int:pk>/update", views.CompanyUpdateView.as_view(), name="company_update"),
    path("company/<int:company_pk>/review", views.ReviewListView.as_view(), name="review_list"),
    path("company/<int:company_pk>/review/<int:pk>/update", views.ReviewUpdateView.as_view(), name="review_update"),
    path("company/<int:company_pk>/message", views.MessageListView.as_view(), name="message_list"),
    path("companies/<int:company_pk>/qr", views.qr, name="qr"),
    path("companies/<int:company_pk>/rate_widget", views.rate_widget, name="rate_widget"),
    path("companies/<int:company_pk>/reviews_widget", views.reviews_widget, name="reviews_widget"),
    path("notifications", views.NotificationListView.as_view(), name="notification_list"),
    path("pref", views.pref, name="pref"),

    path('chartJSON', views.LineChartJSONView.as_view(), name='line_chart_json'),
]
