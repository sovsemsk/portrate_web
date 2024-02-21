from django.urls import path

from . import views

urlpatterns = [
    path("javascript.js", views.javascript, name="widget_javascript"),
]

