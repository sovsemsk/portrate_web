from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from resources.models import Company, Notification

from django.views.generic import ListView


class CompanyListView(ListView):
    template_name = 'dashboard/company_list.html'
    model = Company
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'companies'
        context['host'] = settings.HOST
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(
            is_active=True,
            users__in=(self.request.user,)
        ).order_by('name')
        return queryset


class NotificationListView(ListView):
    template_name = 'dashboard/notification_list.html'
    model = Notification
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'notification_list'
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(
            company__users__in=(self.request.user,)
        ).select_related('company')
        return queryset



# @TODO: Сделать тут кеш
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
def companies(request):
    current_companies = get_current_companies(request.user)
    return render(request, 'dashboard/companies.html', {
        'nav': 'companies',
        'host': settings.HOST,
        'current_companies': current_companies,
        'current_companies_paginator': Paginator(current_companies, 1)
    })


@login_required
@require_http_methods(['GET'])
def notifications(request):
    current_companies = get_current_companies(request.user)
    current_notifications = Notification.objects.filter(
        company__in=current_companies
    ).select_related('company').all()

    return render(request, 'dashboard/notifications.html', {
        'nav': 'notifications',
        'current_companies': current_companies,
        'current_notifications': current_notifications
    })


@login_required
@require_http_methods(['GET'])
def help(request):
    return render(request, 'dashboard/help.html', {
        'nav': 'help'
    })


@login_required
@require_http_methods(['GET'])
def price(request):
    return render(request, 'dashboard/price.html', {
        'nav': 'price'
    })

@login_required
@require_http_methods(['GET'])
def pref(request):
    return render(request, 'dashboard/pref.html', {
        'nav': 'pref'
    })
