from django.urls import path

from .views import rate, create, request, success

urlpatterns = [
    path("<int:pk>/", rate, name="rate"),
    path("<int:pk>/create/", create, name="create"),
    path("<int:pk>/request/", request, name="request"),
    path("<int:pk>/success/", success, name="success")
]
