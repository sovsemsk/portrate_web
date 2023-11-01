from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator

from resources.models import Company, Notification


class CompanyListView(ListView):
    template_name = 'dashboard/company_list.html'
    model = Company
    paginate_by = 5

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(CompanyListView, self).dispatch(request, *args, **kwargs)


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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(NotificationListView, self).dispatch(request, *args, **kwargs)

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
