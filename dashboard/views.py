from datetime import datetime
from urllib.parse import unquote

from celery import chain
from chartjs.views.lines import BaseLineChartView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
from resources.tasks import update_yandex_task, update_gis_task, update_google_task, update_counters_task
from services.search import SearchYandex, SearchGis, SearchGoogle
from .filters import MessageFilter, ReviewFilter, RatingStampFilter
from .forms import (
    CompanyMasterSearchForm,
    CompanyForm,
    CompanyContactForm,
    CompanyDataForm,
    CompanyLinkForm,
    CompanyMembershipFormSet,
    CompanyParserForm,
    DashboardAuthenticationForm,
    DashboardUserChangeForm,
    DashboardSetPasswordForm,
    DashboardUserCreationForm,
    ProfileForm,
    ReviewForm,
)


@login_required
@require_http_methods(["GET", "POST"])
def company_master_yandex(request):
    card_list = []

    if request.method == "POST":
        form = CompanyMasterSearchForm(request.POST)

        if form.is_valid():
            card_list = SearchYandex.search(form.cleaned_data.get("query"))
    else:
        form = CompanyMasterSearchForm()

    return render(request, "dashboard/company_master_yandex.html", {
        "nav": "company",
        "form": form,
        "card_list": card_list
    })


@login_required
@require_http_methods(["GET", "POST"])
def company_master_gis(request):
    card_list = []

    if request.method == "POST":
        form = CompanyMasterSearchForm(request.POST)

        if form.is_valid():
            card_list = SearchGis.search(form.cleaned_data.get("query"))
    else:
        form = CompanyMasterSearchForm()

    return render(request, "dashboard/company_master_gis.html", {
        "nav": "company",
        "form": form,
        "card_list": card_list
    })


@login_required
@require_http_methods(["GET", "POST"])
def company_master_google(request):
    card_list = []

    if request.method == "POST":
        form = CompanyMasterSearchForm(request.POST)

        if form.is_valid():
            card_list = SearchGoogle.search(form.cleaned_data.get("query"))
    else:
        form = CompanyMasterSearchForm()

    return render(request, "dashboard/company_master_google.html", {
        "nav": "company",
        "form": form,
        "card_list": card_list
    })


@login_required
@require_http_methods(["GET", "POST"])
def company_master_data(request):
    address_yandex = request.COOKIES.get("address_yandex", "")
    name_yandex = request.COOKIES.get("name_yandex", "")
    phone_yandex = request.COOKIES.get("phone_yandex", "")
    id_yandex = request.COOKIES.get("id_yandex", None)
    id_gis = request.COOKIES.get("id_gis", None)
    id_google = request.COOKIES.get("id_google", None)

    if request.method == "POST":
        form = CompanyForm(request.POST)

        if form.is_valid():
            parsers_runs = False
            parsers_chain = []

            # Заполнение полей для паресра и запроса отзывов
            if id_yandex:
                form.instance.parser_link_yandex = unquote(f"https://yandex.ru/maps/org/{name_yandex}/{id_yandex}/reviews")
                form.instance.form_link_yandex = unquote(f"https://yandex.ru/maps/org/{name_yandex}/{id_yandex}/reviews?add-review=true")
                form.instance.is_parse_yandex = True

            if id_gis:
                form.instance.parser_link_gis = unquote(f"https://2gis.ru/orenburg/firm/{id_gis}/tab/reviews")
                form.instance.form_link_gis = unquote(f"https://2gis.ru/orenburg/firm/{id_gis}/tab/reviews/addreview")
                form.instance.is_parse_gis = True

            if id_google:
                form.instance.parser_link_google = unquote(f"https://www.google.com/maps/search/?api=1&query=~&query_place_id={id_google}")
                form.instance.form_link_google = unquote(f"https://search.google.com/local/writereview?placeid={id_google}")
                form.instance.is_parse_google = True

            form.save()
            form.instance.users.add(request.user)

            # Первый запуск парсеров
            if form.instance.parser_link_yandex:
                parsers_runs = True
                parsers_chain.append(update_yandex_task.s(company_id=form.instance.id))

            if form.instance.is_parse_gis:
                parsers_runs = True
                parsers_chain.append(update_gis_task.s(company_id=form.instance.id))

            if form.instance.is_parse_google:
                parsers_runs = True
                parsers_chain.append(update_google_task.s(company_id=form.instance.id))

            if parsers_runs:
                parsers_chain.append(update_counters_task.s(company_id=form.instance.id))
                chain(parsers_chain).apply_async()

            # Сообщение и редирект
            messages.success(request, "Компания успешно создана")
            return redirect(reverse("company_detail", kwargs={"pk": form.instance.id}))

    else:
        form = CompanyForm(initial={
            "name": unquote(name_yandex),
            "address": unquote(address_yandex),
            "phone": unquote(phone_yandex)
        })

    return render(request, "dashboard/company_master_data.html", {
        "nav": "company",
        "form": form
    })


class CompanyListView(LoginRequiredMixin, ListView):
    context_object_name = "company_list"
    model = Company
    paginate_by = 30
    template_name = "dashboard/company_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = settings.HOST
        context["nav"] = "company"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(users__in=[self.request.user]).order_by("name")


class CompanyDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "company"
    model = Company
    template_name = "dashboard/company_detail.html"

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
        return queryset.filter(users__in=[self.request.user])


class CompanyParserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyParserForm
    model = Company
    template_name = "dashboard/company_parser_update.html"
    success_message = "Настройки компании успешно сохранены"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = settings.HOST
        context["menu_nav"] = "parser"
        context["nav"] = "company"
        context["tab_nav"] = "update"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_parser_update", kwargs={"pk": self.kwargs["pk"]})


class CompanyDataUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyDataForm
    model = Company
    template_name = "dashboard/company_data_update.html"
    success_message = "Настройки компании успешно сохранены"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = settings.HOST
        context["menu_nav"] = "data"
        context["nav"] = "company"
        context["tab_nav"] = "update"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_data_update", kwargs={"pk": self.kwargs["pk"]})


class CompanyLinkUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyLinkForm
    model = Company
    template_name = "dashboard/company_link_update.html"
    success_message = "Настройки компании успешно сохранены"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = settings.HOST
        context["menu_nav"] = "link"
        context["nav"] = "company"
        context["tab_nav"] = "update"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_link_update", kwargs={"pk": self.kwargs["pk"]})


class CompanyContactUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyContactForm
    model = Company
    template_name = "dashboard/company_contact_update.html"
    success_message = "Настройки компании успешно сохранены"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = settings.HOST
        context["menu_nav"] = "contact"
        context["nav"] = "company"
        context["tab_nav"] = "update"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_contact_update", kwargs={"pk": self.kwargs["pk"]})


class CompanyMembershipUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = CompanyMembershipFormSet
    model = Company
    template_name = "dashboard/company_membership_update.html"
    success_message = "Настройки компании успешно сохранены"

    def get_form(self, form_class=None):
        form = super().get_form(self.form_class)
        form.queryset = form.queryset.filter(user=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = settings.HOST
        context["menu_nav"] = "membership"
        context["nav"] = "company"
        context["tab_nav"] = "update"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_membership_update", kwargs={"pk": self.kwargs["pk"]})


class CompanyRatingDynamic(LoginRequiredMixin, BaseLineChartView):
    def __init__(self, **kwargs):
        super().__init__()
        self.company = None
        self.rating_history = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])
        self.rating_history = RatingStampFilter(
            self.request.GET,
            queryset=RatingStamp.objects.filter(company=self.company)
        ).qs

        return super(CompanyRatingDynamic, self).dispatch(request, *args, **kwargs)

    def get_labels(self):
        range_param = self.request.GET.get("range", "week")
        format_map = {"week": "%d.%m", "month": "%d.%m", "quarter": "%d.%m", "year": "%m.%y", "total": "%m.%y"}
        return list(map(lambda x: x.created_at.strftime(format_map[range_param]), self.rating_history)) or [
            datetime.now().strftime("%d.%m")]

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
        ).order_by("-created_at")


class ReviewUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "review"
    form_class = ReviewForm
    model = Review
    success_message = "Настройки отзыва успешно сохранены"

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
        return f"{reverse('review_list', kwargs={'company_pk': self.kwargs['company_pk']})}?{self.request.GET.urlencode()}"


class MessageListView(LoginRequiredMixin, FilterView):
    context_object_name = "message_list"
    filterset_class = MessageFilter
    model = Message
    paginate_by = 30
    template_name = "dashboard/message_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])
        context["nav"] = "company"
        context["tab_nav"] = "message"
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(company__in=[self.kwargs["company_pk"]],
                               company__users__in=[self.request.user]).select_related("company").order_by("-created_at")


@login_required
@require_http_methods(["GET"])
def qr(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk, users__in=[request.user])
    template = request.GET.get("template", "s")
    theme = request.GET.get("theme", "l")

    return render(
        request,
        "dashboard/qr.html",
        {
            "company": company,
            "nav": "company",
            "tab_nav": "qr",
            "template": template,
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
        form = DashboardAuthenticationForm(request)

    return render(request, "dashboard/user_login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def user_logout(request):
    auth_logout(request)
    return redirect("user_login")
