from django.urls import path

from .views import rate, create, request, success

urlpatterns = [
    path("<int:company_pk>/", rate, name="rate"),
    path("<int:company_pk>/create/", create, name="create"),
    path("<int:company_pk>/request/", request, name="request"),
    path("<int:company_pk>/success/", success, name="success")
]
