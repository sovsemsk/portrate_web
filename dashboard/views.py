from datetime import datetime

from chartjs.views.lines import BaseLineChartView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_filters.views import FilterView

from resources.models import Company, Message, Review, RatingStamp
from resources.tasks import send_telegram_text_task
from .filters import MessageFilter, ReviewFilter, RatingStampFilter
from .forms import (
    CompanyForm,
    CompanyContactForm,
    CompanyDataForm,
    CompanyLinkForm,
    CompanyParserForm,
    DashboardAuthenticationForm,
    DashboardUserChangeForm,
    DashboardSetPasswordForm,
    DashboardUserCreationForm,
    ProfileForm,
    ReviewForm,
)


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
        company = model_to_dict(self.object)
        range_map = {"week": "_week_", "month": "_month_", "quarter": "_quarter_", "year": "_year_", "total": "_"}
        range_param = self.request.GET.get("range", "week")

        context["host"] = settings.HOST
        context["nav"] = "company"
        context["tab_nav"] = "detail"

        if range_param in range_map:
            context["reviews_yandex_positive_count"] = company[f"reviews_yandex_positive{range_map[range_param]}count"]
            context["reviews_yandex_negative_count"] = company[f"reviews_yandex_negative{range_map[range_param]}count"]
            context["reviews_yandex_total_count"] = company[f"reviews_yandex_total{range_map[range_param]}count"]
            context["reviews_gis_positive_count"] = company[f"reviews_gis_positive{range_map[range_param]}count"]
            context["reviews_gis_negative_count"] = company[f"reviews_gis_negative{range_map[range_param]}count"]
            context["reviews_gis_total_count"] = company[f"reviews_gis_total{range_map[range_param]}count"]
            context["reviews_google_positive_count"] = company[f"reviews_google_positive{range_map[range_param]}count"]
            context["reviews_google_negative_count"] = company[f"reviews_google_negative{range_map[range_param]}count"]
            context["reviews_google_total_count"] = company[f"reviews_google_total{range_map[range_param]}count"]

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


class CompanyParserUpdateView(SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyParserForm
    model = Company
    template_name = "dashboard/company_parser_update.html"
    success_message = "Настройки компании успешно сохранены"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyParserUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.filter(users__in=[self.request.user]).order_by("name").all()
        context["company_list"] = companies
        context["host"] = settings.HOST
        context["menu_nav"] = "parser"
        context["nav"] = "company"
        context["tab_nav"] = "update"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=[self.request.user])
        return queryset

    def get_success_url(self):
        return reverse("company_parser_update", kwargs={"pk": self.object.id})


class CompanyDataUpdateView(SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyDataForm
    model = Company
    template_name = "dashboard/company_data_update.html"
    success_message = "Настройки компании успешно сохранены"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyDataUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.filter(users__in=[self.request.user]).order_by("name").all()
        context["company_list"] = companies
        context["host"] = settings.HOST
        context["menu_nav"] = "data"
        context["nav"] = "company"
        context["tab_nav"] = "update"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=[self.request.user])
        return queryset

    def get_success_url(self):
        return reverse("company_data_update", kwargs={"pk": self.object.id})


class CompanyLinkUpdateView(SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyLinkForm
    model = Company
    template_name = "dashboard/company_link_update.html"
    success_message = "Настройки компании успешно сохранены"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyLinkUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.filter(users__in=[self.request.user]).order_by("name").all()
        context["company_list"] = companies
        context["host"] = settings.HOST
        context["menu_nav"] = "link"
        context["nav"] = "company"
        context["tab_nav"] = "update"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=[self.request.user])
        return queryset

    def get_success_url(self):
        return reverse("company_data_update", kwargs={"pk": self.object.id})


class CompanyContactUpdateView(SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyContactForm
    model = Company
    template_name = "dashboard/company_contact_update.html"
    success_message = "Настройки компании успешно сохранены"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyContactUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.filter(users__in=[self.request.user]).order_by("name").all()
        context["company_list"] = companies
        context["host"] = settings.HOST
        context["menu_nav"] = "contact"
        context["nav"] = "company"
        context["tab_nav"] = "update"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(users__in=[self.request.user])
        return queryset

    def get_success_url(self):
        return reverse("company_contact_update", kwargs={"pk": self.object.id})


class CompanyRatingDynamic(BaseLineChartView):
    def __init__(self, **kwargs):
        super().__init__()
        self.company = None
        self.rating_history = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.company = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])

        self.rating_history = RatingStampFilter(
            self.request.GET,
            queryset=RatingStamp.objects.filter(company_id=self.company.id)
        ).qs

        return super(CompanyRatingDynamic, self).dispatch(request, *args, **kwargs)

    def get_labels(self):
        range_param = self.request.GET.get("range", "week")
        format_map = {"week": "%d.%m", "month": "%d.%m", "quarter": "%d.%m", "year": "%m.%y", "total": "%m.%y"}
        return list(map(lambda x: x.created_at.strftime(format_map[range_param]), self.rating_history)) or [datetime.now().strftime("%d.%m")]

    def get_dataset_options(self, index, color):
        default_opt = {
            "backgroundColor": "rgba(255, 95, 0, 0.2)",
            "borderColor": "rgba(0, 0, 0, 0)",
            "pointBackgroundColor": "rgba(255, 95, 0, 1)",
            "pointBorderColor": "rgba(238, 240, 242, 1)",
            "cubicInterpolationMode": "monotone",
            "fill": True,
        }
        return default_opt


class CompanyRatingYandexDynamic(CompanyRatingDynamic):
    def get_providers(self):
        return ["Яндекс"]

    def get_data(self):
        return [list(map(lambda x: x.rating_yandex, self.rating_history)) or [self.company.rating_yandex]]


class CompanyRatingGisDynamic(CompanyRatingDynamic):
    def get_providers(self):
        return ["2Гис"]

    def get_data(self):
        return [list(map(lambda x: x.rating_gis, self.rating_history)) or [self.company.rating_gis]]


class CompanyRatingGoogleDynamic(CompanyRatingDynamic):
    def get_providers(self):
        return ["Google"]

    def get_data(self):
        return [list(map(lambda x: x.rating_google, self.rating_history)) or [self.company.rating_google]]


class ReviewListView(FilterView):
    context_object_name = "review_list"
    filterset_class = ReviewFilter
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
        context["tab_nav"] = "review"
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
        context["tab_nav"] = "review"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(company__in=[self.kwargs["company_pk"]], company__users__in=[self.request.user])

    def get_success_url(self):
        return f"{reverse('review_list', kwargs={'company_pk': self.object.company.id})}?{self.request.GET.urlencode()}"


class MessageListView(FilterView):
    context_object_name = "message_list"
    filterset_class = MessageFilter
    model = Message
    paginate_by = 30
    template_name = "dashboard/message_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])
        context["nav"] = "company"
        context["tab_nav"] = "message"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(
            company__in=[self.kwargs["company_pk"]],
            company__users__in=[self.request.user]
        ).select_related("company").order_by("-created_at")


@login_required
@require_http_methods(["GET"])
def qr(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk, users__in=[request.user])
    orientation = request.GET.get("orientation", "v")
    theme = request.GET.get("theme", "l")

    return render(
        request,
        "dashboard/qr.html",
        {
            "company": company,
            "nav": "company",
            "tab_nav": "qr",
            "orientation": orientation,
            "theme": theme
        }
    )


@login_required
@require_http_methods(["GET"])
def widget_rating(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk, users__in=[request.user])
    theme = request.GET.get("theme", "l")
    position = request.GET.get("position", "lb")

    return render(
        request,
        "dashboard/widget_rating.html",
        {
            "company": company,
            "nav": "company",
            "position": position,
            "tab_nav": "widget_rating",
            "theme": theme
        }
    )


@login_required
@require_http_methods(["GET"])
def widget_reviews(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk, users__in=[request.user])
    layout = request.GET.get("layout", "s")
    theme = request.GET.get("theme", "l")

    return render(
        request,
        "dashboard/widget_reviews.html",
        {
            "company": company,
            "layout": layout,
            "nav": "company",
            "tab_nav": "widget_reviews",
            "theme": theme
        }
    )


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Настройки профиля успешно сохранены")

    else:
        form = ProfileForm(instance=request.user.profile)

    return render(
        request,
        "dashboard/profile.html",
        {
            "form": form,
            "nav": "settings",
            "tab_nav": "profile",
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def rate(request):
    return render(
        request,
        "dashboard/rate.html",
        {
            "nav": "finance",
            "tab_nav": "rate",
        }
    )


@login_required
@require_http_methods(["GET", "POST"])
def billing(request):
    return render(
        request,
        "dashboard/billing.html",
        {
            "nav": "finance",
            "tab_nav": "billing",
        }
    )


@login_required
@require_http_methods(["GET", "POST"])
def account(request):
    if request.method == "POST":
        form = DashboardUserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Настройки аккаунта успешно сохранены")

    else:
        form = DashboardUserChangeForm(instance=request.user)

    return render(request, "dashboard/account.html", {
        "nav": "settings",
        "tab_nav": "account",
        "form": form
    })


@login_required
@require_http_methods(["GET", "POST"])
def security(request):
    if request.method == "POST":
        form = DashboardSetPasswordForm(request.user, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Настройки безопасности успешно сохранены")

    else:
        form = DashboardSetPasswordForm(request.user)

    return render(request, "dashboard/security.html", {
        "nav": "settings",
        "tab_nav": "security",
        "form": form
    })


@require_http_methods(["GET", "POST"])
def user_create(request):
    if request.method == "POST":
        form = DashboardUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("user_login")
        else:
            return render(request, "dashboard/user_create.html", {"form": form})

    else:
        form = DashboardUserCreationForm()
        return render(request, "dashboard/user_create.html", {"form": form})


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == "POST":
        form = DashboardAuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.user_cache)
            return redirect("company_list")
        else:
            return render(request, "dashboard/user_login.html", {"form": form})

    else:
        form = DashboardAuthenticationForm(request)
        return render(request, "dashboard/user_login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def user_logout(request):
    auth_logout(request)
    return redirect("user_login")


@login_required
@require_http_methods(("GET",))
def telegram_notify_unsubscribe(request):
    send_telegram_text_task(request.user.profile.telegram_id, "👋🏼 Вы отписаны от уведомлений telegram")
    request.user.profile.telegram_id = None
    request.user.profile.save()

    return redirect(request.GET.get("next"))
