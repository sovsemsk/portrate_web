from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator

from resources.models import Company, NegativeMessage, Notification, Review


class CompanyListView(ListView):
    template_name = 'dashboard/company_list.html'
    model = Company
    context_object_name = 'company_list'
    paginate_by = 5


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyListView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'company'
        context['host'] = settings.HOST
        return context


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(
            is_active=True,
            users__in=(self.request.user,)
        ).order_by('name')
        return queryset


class CompanyDetailView(DetailView):
    template_name = 'dashboard/company_detail.html'
    model = Company
    context_object_name = 'company'


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyDetailView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'company'
        context['sub_nav'] = 'detail'
        context['host'] = settings.HOST
        return context


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(
            is_active=True,
            users__in=(self.request.user,)
        )
        return queryset


class ReviewListView(ListView):
    template_name = 'dashboard/review_list.html'
    model = Review
    context_object_name = 'review_list'
    paginate_by = 5


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReviewListView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, pk=self.kwargs['company_pk'])
        context['nav'] = 'company'
        context['sub_nav'] = 'review'
        return context


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        company = get_object_or_404(Company, pk=self.kwargs['company_pk'])
        queryset = queryset.filter(
            company__in=(company.id,),
            company__users__in=(self.request.user,)
        ).select_related('company').order_by('-created_at')
        return queryset


class MessageListView(ListView):
    template_name = 'dashboard/message_list.html'
    model = NegativeMessage
    context_object_name = 'message_list'
    paginate_by = 5


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageListView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, pk=self.kwargs['company_pk'])
        context['nav'] = 'company'
        context['sub_nav'] = 'message'
        return context


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        company = get_object_or_404(Company, pk=self.kwargs['company_pk'])
        queryset = queryset.filter(
            company__in=(company.id,),
            company__users__in=(self.request.user,)
        ).select_related('company').order_by('-created_at')
        return queryset


class NotificationListView(ListView):
    template_name = 'dashboard/notification_list.html'
    model = Notification
    context_object_name = 'notification_list'
    paginate_by = 10


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationListView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'notification'
        return context


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(
            company__users__in=(self.request.user,)
        ).select_related('company').order_by('-created_at')
        return queryset


@login_required
@require_http_methods(['GET'])
def qr(request, company_pk):
    return render(request, 'dashboard/qr_list.html', {
        'company': get_object_or_404(Company, pk=company_pk),
        'nav': 'company',
        'sub_nav': 'qr'
    })


@login_required
@require_http_methods(['GET'])
def widget(request, company_pk):
    return render(request, 'dashboard/widget_list.html', {
        'company': get_object_or_404(Company, pk=company_pk),
        'nav': 'company',
        'sub_nav': 'widget'
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
