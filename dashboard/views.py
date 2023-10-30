from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from resources.models import Company, Notification


@login_required
@require_http_methods(['GET'])
def index(request):
    companies = Company.objects.filter(users__in=(request.user,)).all()
    return render(request, 'dashboard/index.html', {
        'nav': 'index',
        'companies': companies
    })


@login_required
@require_http_methods(['GET'])
def companies(request):
    companies = Company.objects.filter(users__in=(request.user,)).all()
    return render(request, 'dashboard/companies.html', {
        'nav': 'companies',
        'companies': companies
    })


@login_required
@require_http_methods(['GET'])
def notifications(request):
    companies = Company.objects.filter(users__in=(request.user,)).all()
    notifications = Notification.objects.filter(company__in=companies).all()
    return render(request, 'dashboard/notifications.html', {
        'nav': 'notifications',
        'companies': companies,
        'notifications': notifications
    })
