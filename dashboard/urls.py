from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company_list'),
    path('company/<int:pk>', views.CompanyDetailView.as_view(), name='company_detail'),
    path('company/<int:company_pk>/review', views.ReviewListView.as_view(), name='review_list'),
    path('company/<int:company_pk>/message', views.MessageListView.as_view(), name='message_list'),
    # path('companies/<int:id>/sms', views.SmsListView.as_view(), name='sms_list'),
    # path('companies/<int:id>/qr', views.QrListView.as_view(), name='qr_list'),
    # path('companies/<int:id>/widget', views.WidgetListView.as_view(), name='widget_list'),
    path('help', views.help, name='dashboard_help'),
    path('price', views.price, name='dashboard_price'),
    path('notifications', views.NotificationListView.as_view(), name='notification_list'),
    path('pref', views.pref, name='dashboard_pref'),
]
