from django.urls import path
from . import views

urlpatterns = [
    path('', views.companies, name='dashboard_companies'),
    path('help', views.help, name='dashboard_help'),
    path('price', views.price, name='dashboard_price'),
    path('notifications', views.notifications, name='dashboard_notifications'),
    path('pref', views.pref, name='dashboard_pref'),
]
