from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company-list'),
    path('help', views.help, name='dashboard_help'),
    path('price', views.price, name='dashboard_price'),
    path('notifications', views.NotificationListView.as_view(), name='notifications-list'),
    path('pref', views.pref, name='dashboard_pref'),
]
