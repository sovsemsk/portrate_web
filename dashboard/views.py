from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def index(request):
    print(request.user)
    return render(request, 'dashboard/index.html')
