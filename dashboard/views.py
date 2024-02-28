from chartjs.views.lines import BaseLineChartView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from dashboard.forms import CompanyForm, ProfileForm, ReviewForm
from resources.models import Company, NegativeMessage, Notification, Review


class CompanyListView(ListView):
    context_object_name = "company_list"
    model = Company
    paginate_by = 30
    template_name = "dashboard/company_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = settings.HOST
        context["nav"] = "company"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=[self.request.user]).order_by("name")
        return queryset


class CompanyDetailView(DetailView):
    context_object_name = "company"
    model = Company
    template_name = "dashboard/company_detail.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = settings.HOST
        context["nav"] = "company"
        context["sub_nav"] = "detail"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=[self.request.user])
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
        companies = Company.objects.filter(users__in=[self.request.user]).order_by("name").all()
        context["company_list"] = companies
        context["host"] = settings.HOST
        context["nav"] = "company"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=[self.request.user])
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
    success_message = "Настройки компании успешно сохранены"
    template_name = "dashboard/company_update.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.filter(users__in=[self.request.user]).order_by("name").all()
        context["company_list"] = companies
        context["host"] = settings.HOST
        context["nav"] = "company"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=[self.request.user])
        return queryset

    def get_success_url(self):
        return reverse("company_update", kwargs={"pk": self.object.id})


class ReviewListView(ListView):
    context_object_name = "review_list"
    paginate_by = 30
    model = Review
    template_name = "dashboard/review_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReviewListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])
        context["nav"] = "company"
        context["sub_nav"] = "review"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(
            company__in=[self.kwargs["company_pk"]],
            company__users__in=[self.request.user]
        ).select_related("company").order_by("-created_at")


class ReviewUpdateView(SuccessMessageMixin, UpdateView):
    context_object_name = "review"
    form_class = ReviewForm
    model = Review
    success_message = "Настройки отзыва успешно сохранены"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReviewUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])
        context["nav"] = "company"
        context["sub_nav"] = "review"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(company__in=[self.kwargs["company_pk"]], company__users__in=[self.request.user])

    def get_success_url(self):
        return reverse("review_list", kwargs={"company_pk": self.object.company.id})


class MessageListView(ListView):
    context_object_name = "message_list"
    model = NegativeMessage
    paginate_by = 30
    template_name = "dashboard/message_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])
        context["nav"] = "company"
        context["sub_nav"] = "message"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(
            company__in=[self.kwargs["company_pk"]],
            company__users__in=[self.request.user]
        ).select_related("company").order_by("-created_at")


class NotificationListView(ListView):
    template_name = "dashboard/notification_list.html"
    model = Notification
    context_object_name = "notification_list"
    paginate_by = 30

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "notification"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(company__users__in=[self.request.user]).select_related("company").order_by("-created_at")


@login_required
@require_http_methods(["GET"])
def qr(request, company_pk):
    dark = bool(request.GET.get("dark", False))

    return render(
        request,
        "dashboard/qr.html",
        {
            "company": get_object_or_404(Company, pk=company_pk),
            "nav": "company",
            "sub_nav": "qr",
            "dark": dark
        }
    )


@login_required
@require_http_methods(["GET"])
def rate_widget(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk, users__in=[request.user])
    theme = request.GET.get("theme", "light")
    position = request.GET.get("position", "lb")

    return render(
        request,
        "dashboard/rate_widget.html",
        {
            "company": company,
            "nav": "company",
            "position": position,
            "sub_nav": "rate_widget",
            "theme": theme
        }
    )


@login_required
@require_http_methods(["GET"])
def reviews_widget(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk, users__in=[request.user])
    theme = request.GET.get("theme", "light")

    return render(
        request,
        "dashboard/reviews_widget.html",
        {
            "company": company,
            "nav": "company",
            "sub_nav": "reviews_widget",
            "theme": theme
        }
    )


@login_required
@require_http_methods(["GET", "POST"])
def pref(request):
    company_list = Company.objects.filter(users__in=(request.user,)).order_by("name").all()

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


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Яндекс", "2Гис", "Google"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[4.1, 4.2, 4.3, 4.4, 4.4, 4.7, 4.8],
                [4.7, 4.6, 4.5, 4.4, 4.3, 4.1, 4.2],
                [4.9, 5.0, 5.0, 4.9, 4.8, 4.7, 4.6]]