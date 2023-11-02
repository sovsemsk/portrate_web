from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company_list'),
    path('companies/<int:pk>', views.CompanyDetailView.as_view(), name='company_detail'),
    # path('companies/<int:id>/reviews', views.ReviewsListView.as_view(), name='reviews_list'),
    # path('companies/<int:id>/messages', views.MessagesListView.as_view(), name='messages_list'),
    # path('companies/<int:id>/sms', views.SmsListView.as_view(), name='sms_list'),
    path('help', views.help, name='dashboard_help'),
    path('price', views.price, name='dashboard_price'),
    path('notifications', views.NotificationListView.as_view(), name='notification_list'),
    path('pref', views.pref, name='dashboard_pref'),
]
