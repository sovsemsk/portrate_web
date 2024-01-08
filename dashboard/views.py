from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from resources.models import Company, NegativeMessage, Notification, Review

from dashboard.forms import CompanyForm, ProfileForm


class CompanyListView(ListView):
    template_name = "dashboard/company_list.html"
    model = Company
    context_object_name = "company_list"
    paginate_by = 5

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "company"
        context["host"] = settings.HOST
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=(self.request.user,)).order_by("name")
        return queryset


class CompanyDetailView(DetailView):
    template_name = "dashboard/company_detail.html"
    model = Company
    context_object_name = "company"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "company"
        context["sub_nav"] = "detail"
        context["host"] = settings.HOST
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=(self.request.user,))
        return queryset


class CompanyCreateView(SuccessMessageMixin, CreateView):
    context_object_name = "company"
    form_class = CompanyForm
    model = Company
    success_message = "Компания успешно создана"
    template_name = "dashboard/company_create.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = (
            Company.objects.filter(users__in=(self.request.user,))
            .order_by("name")
            .all()
        )

        context["nav"] = "company"
        context["sub_nav"] = "update"
        context["host"] = settings.HOST
        context["company_list"] = companies
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=(self.request.user,))
        return queryset

    def form_valid(self, form, **kwargs):
        response = super(CompanyCreateView, self).form_valid(form, **kwargs)
        self.object.is_active = True
        self.object.users.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse("company_update", kwargs={"pk": self.object.id})


class CompanyUpdateView(SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyForm
    model = Company
    success_message = "Настройки успешно сохранены"
    template_name = "dashboard/company_update.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        companies = (
            Company.objects.filter(users__in=(self.request.user,))
            .order_by("name")
            .all()
        )

        context["nav"] = "pref"
        context["sub_nav"] = "update"
        context["host"] = settings.HOST
        context["company_list"] = companies
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=(self.request.user,))
        return queryset

    def get_success_url(self):
        return reverse("company_update", kwargs={"pk": self.object.id})


class ReviewListView(ListView):
    template_name = "dashboard/review_list.html"
    model = Review
    context_object_name = "review_list"
    paginate_by = 5

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReviewListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"])
        context["nav"] = "company"
        context["sub_nav"] = "review"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        company = get_object_or_404(Company, pk=self.kwargs["company_pk"])
        queryset = (
            queryset.filter(
                company__in=(company.id,), company__users__in=(self.request.user,)
            )
            .select_related("company")
            .order_by("-created_at")
        )
        return queryset


class MessageListView(ListView):
    template_name = "dashboard/message_list.html"
    model = NegativeMessage
    context_object_name = "message_list"
    paginate_by = 5

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"])
        context["nav"] = "company"
        context["sub_nav"] = "message"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        company = get_object_or_404(Company, pk=self.kwargs["company_pk"])
        queryset = (
            queryset.filter(
                company__in=(company.id,), company__users__in=(self.request.user,)
            )
            .select_related("company")
            .order_by("-created_at")
        )
        return queryset


class NotificationListView(ListView):
    template_name = "dashboard/notification_list.html"
    model = Notification
    context_object_name = "notification_list"
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "notification"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = (
            queryset.filter(company__users__in=(self.request.user,))
            .select_related("company")
            .order_by("-created_at")
        )
        return queryset


@login_required
@require_http_methods(["GET"])
def qr(request, company_pk):
    return render(
        request,
        "dashboard/qr_list.html",
        {
            "company": get_object_or_404(Company, pk=company_pk),
            "nav": "company",
            "sub_nav": "qr",
        },
    )


@login_required
@require_http_methods(["GET"])
def widget(request, company_pk):
    return render(
        request,
        "dashboard/widget_list.html",
        {
            "company": get_object_or_404(Company, pk=company_pk),
            "nav": "company",
            "sub_nav": "widget",
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def pref(request):
    company_list = (
        Company.objects.filter(users__in=(request.user,)).order_by("name").all()
    )

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Настройки успешно сохранены")

    else:
        form = ProfileForm(instance=request.user.profile)

    return render(
        request,
        "dashboard/pref.html",
        {
            "company_list": company_list,
            "form": form,
            "nav": "pref",
            "sub_nav": "notification",
        },
    )
