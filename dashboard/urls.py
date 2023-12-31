from django.urls import path

from . import views

urlpatterns = [
    path("", views.CompanyListView.as_view(), name="company_list"),
    path("company/create", views.CompanyCreateView.as_view(), name="company_create"),
    path("company/<int:pk>", views.CompanyDetailView.as_view(), name="company_detail"),
    path(
        "company/<int:pk>/update",
        views.CompanyUpdateView.as_view(),
        name="company_update",
    ),
    path(
        "company/<int:company_pk>/review",
        views.ReviewListView.as_view(),
        name="review_list",
    ),
    path(
        "company/<int:company_pk>/message",
        views.MessageListView.as_view(),
        name="message_list",
    ),
    # path('companies/<int:company_pk>/qr', views.QrListView.as_view(), name='qr_list'),
    # path('companies/<int:company_pk>/widget', views.WidgetListView.as_view(), name='widget_list'),
    path("companies/<int:company_pk>/qr", views.qr, name="qr_list"),
    path("companies/<int:company_pk>/widget", views.widget, name="widget_list"),
    path(
        "notifications", views.NotificationListView.as_view(), name="notification_list"
    ),
    path("pref", views.pref, name="dashboard_pref"),
]
