from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from resources.models import Company, Notification


def get_first_company(user):
    return Company.objects.filter(
        users__in=(user,)
    ).order_by('name').first()


def get_current_company(user, id):
    return Company.objects.filter(
        users__in=(user,),
        id=id
    ).order_by('name').first()


def get_current_companies(user):
    return Company.objects.filter(
        users__in=(user,),
    ).order_by('name').all()


@login_required
@require_http_methods(['GET'])
def index(request):
    company = get_first_company(user=request.user)
    return redirect('dashboard_statistics', company_id=company.id)


@login_required
@require_http_methods(['GET'])
def statistics(request, company_id):
    current_companies = get_current_companies(request.user)

    current_notifications = Notification.objects.filter(
        company__in=current_companies
    ).all()

    return render(request, 'dashboard/dashboard_statistics.html', {
        'nav': 'statistics',
        'current_company': get_current_company(request.user, company_id),
        'current_companies': current_companies,
        'current_notifications': current_notifications
    })


@login_required
@require_http_methods(['GET'])
def companies(request):
    return render(request, 'dashboard/companies.html', {
        'nav': 'companies',
        'current_companies': get_current_companies(request.user),
    })


@login_required
@require_http_methods(['GET'])
def notifications(request):
    current_companies = get_current_companies(request.user)

    notifications = Notification.objects.filter(
        company__in=current_companies
    ).all()

    return render(request, 'dashboard/notifications.html', {
        'nav': 'notifications',
        'current_companies': current_companies,
        'notifications': notifications
    })
