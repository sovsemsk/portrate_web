from datetime import datetime, timedelta, timezone
from functools import reduce
from urllib.parse import unquote

from celery import chain
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, F, Prefetch, Sum, Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView
from django_filters.views import FilterView
from djmoney.money import Money

from billing.tbank import Tbank
from pdf.utils import make_stick, make_card, make_qr
from resources.models import Company, Message, Payment, Review, Service, Story, StorySlide
from resources.tasks import parse_yandex_task, parse_gis_task, parse_google_task
from services.search import SearchGis, SearchGoogle, SearchYandex
from .filters import MessageFilter, ReviewFilter
from .forms import (
    DashboardAuthenticationForm,
    DashboardBusinessRequestCreationForm,
    DashboardCompanyChangeAvitoForm,
    DashboardCompanyChangeContactForm,
    DashboardCompanyChangeDataForm,
    DashboardCompanyChangeFlampForm,
    DashboardCompanyChangeGisForm,
    DashboardCompanyChangeGoogleForm,
    DashboardCompanyChangeIrecommendForm,
    DashboardCompanyChangeOtzovikForm,
    DashboardCompanyChangeProdoctorovForm,
    DashboardCompanyChangeServiceForm,
    DashboardCompanyChangeTextForm,
    DashboardCompanyChangeTripadvisorForm,
    DashboardCompanyChangeVisibleForm,
    DashboardCompanyChangeYandexForm,
    DashboardCompanyChangeYandexServicesForm,
    DashboardCompanyChangeYellForm,
    DashboardCompanyChangeZoonForm,
    DashboardCompanyCreationForm,
    DashboardCompanyCreationLinkYandexForm,
    DashboardCompanyCreationLinkGisForm,
    DashboardCompanyCreationLinkGoogleForm,
    DashboardMembershipChangeFormSet,
    DashboardPasswordChangeForm,
    DashboardProfileChangeForm,
    DashboardProfileChangeRateForm,
    DashboardReviewChangeForm,
    DashboardSearchForm,
    DashboardUserChangeForm,
    DashboardUserCreationForm
)


def company_list_short(user, pk):
    return Company.objects.filter(users__in=[user]).exclude(pk=pk).values("id", "name").order_by("name")[:15]


def story_list(user, nav):
    return Story.objects.filter(** {
        "is_active": True,
        f"is_visible_{nav}": True
    }).prefetch_related(
        Prefetch(
            "users",
            to_attr="users_is_seen",
            queryset=User.objects.filter(pk=user.id)
        )
    ).prefetch_related(
        Prefetch(
            "storyslide_set",
            queryset=StorySlide.objects.order_by("sort")
        )
    ).order_by("-created_at").all


class NoCompanyError(Exception):
    def __init__(self, *args):
        ...

    def __str__(self):
        return "NoCompanyError"


class OneCompanyError(Exception):
    def __init__(self, *args):
        ...

    def __str__(self):
        return "OneCompanyError"


class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = DashboardCompanyCreationForm
    model = Company
    template_name = "dashboard/company_create.html"
    success_message = "Филиал успешно добавлен"

    def dispatch(self, *args, **kwargs):
        profile = args[0].user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.request.session.get("parser_link_yandex", False):
            form.instance.parser_link_yandex = unquote(self.request.session["parser_link_yandex"])
            form.instance.parser_last_change_at_yandex = datetime.now(timezone.utc)

        if self.request.session.get("parser_link_gis", False):
            form.instance.parser_link_gis = unquote(self.request.session["parser_link_gis"])
            form.instance.parser_last_change_at_gis = datetime.now(timezone.utc)

        if self.request.session.get("parser_link_google", False):
            form.instance.parser_link_google = unquote(self.request.session["parser_link_google"])
            form.instance.parser_last_change_at_google = datetime.now(timezone.utc)

        """ Сохранение обьекта филиала """
        form_valid = super().form_valid(form)
        form.instance.users.add(self.request.user)

        """ Инициализация и сохранение флага владельца филиала """
        self.request.user.membership_set.filter(company=self.object).update(is_owner=True)
        return form_valid

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["nav"] = "master"
        context["sub_nav"] = "data"
        return context

    def get_success_url(self):
        return reverse("company_detail", kwargs={"pk": self.object.id})


class CompanyCreateLinkYandexView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        form = DashboardCompanyCreationLinkYandexForm()

        return render(
            request,
            "dashboard/company_create_link_yandex.html",
            {
                "form": form,
                "nav": "master",
                "sub_nav": "yandex"
            }
        )

    def post(self, request):
        profile = request.user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        form = DashboardCompanyCreationLinkYandexForm(request.POST)

        if form.is_valid():
            request.session["parser_link_yandex"] = form.cleaned_data.get("parser_link_yandex")
            return redirect("company_create_link_gis")

        return render(
            request,
            "dashboard/company_create_link_yandex.html",
            {
                "form": form,
                "nav": "master",
                "sub_nav": "yandex"
            }
        )


class CompanyCreateLinkGisView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        form = DashboardCompanyCreationLinkGisForm()

        return render(
            request,
            "dashboard/company_create_link_gis.html",
            {
                "form": form,
                "nav": "master",
                "sub_nav": "gis"
            }
        )

    def post(self, request):
        profile = request.user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        form = DashboardCompanyCreationLinkGisForm(request.POST)

        if form.is_valid():
            request.session["parser_link_gis"] = form.cleaned_data.get("parser_link_gis")
            return redirect("company_create_link_google")

        return render(
            request,
            "dashboard/company_create_link_gis.html",
            {
                "form": form,
                "nav": "master",
                "sub_nav": "gis"
            }
        )


class CompanyCreateLinkGoogleView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        form = DashboardCompanyCreationLinkGoogleForm()

        return render(
            request,
            "dashboard/company_create_link_google.html",
            {
                "form": form,
                "nav": "master",
                "sub_nav": "google"
            }
        )

    def post(self, request):
        profile = request.user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        form = DashboardCompanyCreationLinkGoogleForm(request.POST)

        if form.is_valid():
            request.session["parser_link_google"] = form.cleaned_data.get("parser_link_google")
            return redirect("company_create")

        return render(
            request,
            "dashboard/company_create_link_google.html",
            {
                "form": form,
                "nav": "master",
                "sub_nav": "google"
            }
        )


class CompanyDetailQrView(LoginRequiredMixin, View):
    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk, users__in=[self.request.user])

        if not company.is_active:
            return redirect("profile_update_finance")

        return render(
            request,
            "dashboard/company_qr.html", {
                "company": company,
                "company_list_short": company_list_short(request.user, company.id),
                "nav": "qr"
            }
        )

    def post(self, request, pk):
        company = get_object_or_404(Company, pk=pk, users__in=[self.request.user])

        if not company.is_active:
            return redirect("profile_update_finance")

        theme = request.POST.get("theme", "light")
        layout = request.POST.get("layout", "stick")

        if theme not in ["light", "dark"] or layout not in ["stick", "card", "qr"]:
            raise Http404

        if layout == "stick":
            file = make_stick(company, theme)
        elif layout == "card":
            file = make_card(company, theme)
        elif layout == "qr":
            file = make_qr(company, theme)

        response = HttpResponse(file.getbuffer(), content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename=\"{layout}-{theme}.pdf\""
        return response


class CompanyDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "company"
    model = Company
    template_name = "dashboard/company_detail.html"

    def dispatch(self, *args, **kwargs):
        if not self.get_object().is_active:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        days_ago_param = self.request.GET.get("days_ago", "total")
        days_ago_filter = {}

        if days_ago_param != "total":
            days_ago_filter["created_at__lte"] = datetime.today()
            days_ago_filter["created_at__gte"] = datetime.today() - timedelta(days=int(days_ago_param))

        visit_stamp_count = self.object.visitstamp_set.filter(
            **days_ago_filter
        ).values(
            "utm_source"
        ).annotate(
            count=Count("utm_source")
        ).order_by(
            "utm_source"
        )

        click_stamp_count = self.object.clickstamp_set.filter(
            **days_ago_filter
        ).values(
            "service"
        ).annotate(
            utm_source=F("visit_stamp__utm_source")
        ).annotate(
            count=Count("service")
        ).order_by(
            "utm_source",
            "service"
        )

        context["visit_stamp_list"] = list(
            map(
                lambda visit_stamp: {
                    "visit_stamp_label": visit_stamp["utm_source"],
                    "visit_stamp_count": visit_stamp["count"],
                    "click_stamp_count": reduce(
                        lambda a, b: {"count": a["count"] + b["count"]},
                        list(
                            filter(
                                lambda click_stamp: click_stamp["utm_source"] == visit_stamp["utm_source"],
                                click_stamp_count
                            )
                        ) or [{"count": 0}]
                    )["count"],
                    "click_stamp_list": list(
                        map(
                            lambda click_stamp: {
                                "click_stamp_label": Service[click_stamp["service"]].label,
                                "click_stamp_value": click_stamp["service"],
                                "click_stamp_count": click_stamp["count"]
                            },
                            list(
                                filter(
                                    lambda click_stamp: click_stamp["utm_source"] == visit_stamp["utm_source"],
                                    click_stamp_count
                                )
                            )
                        )
                    )
                },
                visit_stamp_count
            )
        )

        context["visit_stamp_list"].append({
            "visit_stamp_count_total": reduce(
                lambda a, b: {
                    "count": a["count"] + b["count"]
                },
                visit_stamp_count or [{"count": 0}])["count"],
            "click_stamp_count_total": reduce(
                lambda a, b: {
                    "count": a["count"] + b["count"]
                },
                click_stamp_count or [{"count": 0}])["count"]
        })

        context["company_list_short"] = company_list_short(self.request.user, self.object.id)
        context["days_ago_param"] = days_ago_param
        context["nav"] = "statistic"
        return context

    def get_queryset(self):
        days_ago_param = self.request.GET.get("days_ago", "total")
        days_ago_filter = {}

        if days_ago_param != "total":
            days_ago_filter["review__created_at__lte"] = datetime.today()
            days_ago_filter["review__created_at__gte"] = datetime.today() - timedelta(days=int(days_ago_param))

        return super().get_queryset().filter(
            users__in=[self.request.user]
        ).annotate(
            reviews_count_positive_yandex=Count(
                "review", filter=Q(review__service=Service.YANDEX, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_yandex=Count(
                "review", filter=Q(review__service=Service.YANDEX, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_yandex=Count(
                "review", filter=Q(review__service=Service.YANDEX, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_gis=Count(
                "review", filter=Q(review__service=Service.GIS, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_gis=Count(
                "review", filter=Q(review__service=Service.GIS, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_gis=Count(
                "review", filter=Q(review__service=Service.GIS, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_google=Count(
                "review", filter=Q(review__service=Service.GOOGLE, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_google=Count(
                "review", filter=Q(review__service=Service.GOOGLE, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_google=Count(
                "review", filter=Q(review__service=Service.GOOGLE, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_avito=Count(
                "review", filter=Q(review__service=Service.AVITO, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_avito=Count(
                "review", filter=Q(review__service=Service.AVITO, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_avito=Count(
                "review", filter=Q(review__service=Service.AVITO, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_zoon=Count(
                "review", filter=Q(review__service=Service.ZOON, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_zoon=Count(
                "review", filter=Q(review__service=Service.ZOON, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_zoon=Count(
                "review", filter=Q(review__service=Service.ZOON, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_flamp=Count(
                "review", filter=Q(review__service=Service.FLAMP, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_flamp=Count(
                "review", filter=Q(review__service=Service.FLAMP, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_flamp=Count(
                "review", filter=Q(review__service=Service.FLAMP, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_yell=Count(
                "review", filter=Q(review__service=Service.YELL, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_yell=Count(
                "review", filter=Q(review__service=Service.YELL, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_yell=Count(
                "review", filter=Q(review__service=Service.YELL, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_prodoctorov=Count(
                "review", filter=Q(review__service=Service.PRODOCTOROV, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_prodoctorov=Count(
                "review", filter=Q(review__service=Service.PRODOCTOROV, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_prodoctorov=Count(
                "review", filter=Q(review__service=Service.PRODOCTOROV, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_yandex_services=Count(
                "review", filter=Q(review__service=Service.YANDEX_SERVICES, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_yandex_services=Count(
                "review", filter=Q(review__service=Service.YANDEX_SERVICES, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_yandex_services=Count(
                "review", filter=Q(review__service=Service.YANDEX_SERVICES, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_otzovik=Count(
                "review", filter=Q(review__service=Service.OTZOVIK, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_otzovik=Count(
                "review", filter=Q(review__service=Service.OTZOVIK, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_otzovik=Count(
                "review", filter=Q(review__service=Service.OTZOVIK, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_irecommend=Count(
                "review", filter=Q(review__service=Service.IRECOMMEND, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_irecommend=Count(
                "review", filter=Q(review__service=Service.IRECOMMEND, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_irecommend=Count(
                "review", filter=Q(review__service=Service.IRECOMMEND, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive_tripadvisor=Count(
                "review", filter=Q(review__service=Service.TRIPADVISOR, review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative_tripadvisor=Count(
                "review", filter=Q(review__service=Service.TRIPADVISOR, review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total_tripadvisor=Count(
                "review", filter=Q(review__service=Service.TRIPADVISOR, **days_ago_filter)
            )
        ).annotate(
            reviews_count_positive=Count(
                "review", filter=Q(review__stars__gt=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_negative=Count(
                "review", filter=Q(review__stars__lte=3, **days_ago_filter)
            )
        ).annotate(
            reviews_count_total=Count(
                "review", filter=Q(**days_ago_filter)
            )
        )


class CompanyListView(LoginRequiredMixin, ListView):
    allow_empty = False
    context_object_name = "company_list"
    model = Company
    paginate_by = 30
    template_name = "dashboard/company_list.html"

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Http404:
            return redirect("company_create_link_yandex")

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["nav"] = "home"
        context["story_list"] = story_list(self.request.user, context["nav"])
        return context

    def get_ordering(self):
        return "name"

    def get_queryset(self):
        return super().get_queryset().filter(
            users__in=[self.request.user]
        ).annotate(
            reviews_count_total_yandex=Count("review", filter=Q(review__service=Service.YANDEX))
        ).annotate(
            reviews_count_total_gis=Count("review", filter=Q(review__service=Service.GIS))
        ).annotate(
            reviews_count_total_google=Count("review", filter=Q(review__service=Service.GOOGLE))
        )


class CompanyUpdateFeedbackContactView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = DashboardCompanyChangeContactForm
    model = Company
    success_message = "Филиал успешно обновлен"
    template_name = "dashboard/company_update_feedback_contact.html"

    def dispatch(self, *args, **kwargs):
        if not self.get_object().is_active:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["company_list_short"] = company_list_short(self.request.user, self.object.id)
        context["nav"] = "feedback"
        context["sub_nav"] = "contact"
        return context

    def get_queryset(self):
        return super().get_queryset().filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_update_feedback_contact", kwargs={"pk": self.kwargs["pk"]})


class CompanyUpdateFeedbackDataView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = DashboardCompanyChangeDataForm
    model = Company
    success_message = "Филиал успешно обновлен"
    template_name = "dashboard/company_update_feedback_data.html"

    def dispatch(self, *args, **kwargs):
        if not self.get_object().is_active:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["company_list_short"] = company_list_short(self.request.user, self.object.id)
        context["nav"] = "feedback"
        context["sub_nav"] = "main"
        return context

    def get_queryset(self):
        return super().get_queryset().filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_update_feedback_data", kwargs={"pk": self.kwargs["pk"]})


class CompanyUpdateFeedbackTextView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = DashboardCompanyChangeTextForm
    model = Company
    success_message = "Филиал успешно обновлен"
    template_name = "dashboard/company_update_feedback_text.html"

    def dispatch(self, *args, **kwargs):
        if not self.get_object().is_active:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["company_list_short"] = company_list_short(self.request.user, self.object.id)
        context["nav"] = "feedback"
        context["sub_nav"] = "text"
        return context

    def get_queryset(self):
        return super().get_queryset().filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_update_feedback_text", kwargs={"pk": self.kwargs["pk"]})


class CompanyUpdateFeedbackServiceView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = DashboardCompanyChangeServiceForm
    model = Company
    success_message = "Филиал успешно обновлен"
    template_name = "dashboard/company_update_feedback_service.html"

    def dispatch(self, *args, **kwargs):
        if not self.get_object().is_active:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["company_list_short"] = company_list_short(self.request.user, self.object.id)
        context["nav"] = "feedback"
        context["sub_nav"] = "service"
        return context

    def get_queryset(self):
        return super().get_queryset().filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_update_feedback_service", kwargs={"pk": self.kwargs["pk"]})


class CompanyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    model = Company
    success_message = "Филиал успешно обновлен"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)

        if self.object.is_parser_link_yandex_disabled and self.form_class == DashboardCompanyChangeYandexForm:
            messages.error(self.request, "Ссылка на филиал в Яндекс сегодня уже обновлялась")

        if self.object.is_parser_link_gis_disabled and self.form_class == DashboardCompanyChangeGisForm:
            messages.error(self.request, "Ссылка на филиал в 2Гис сегодня уже обновлялась")

        if self.object.is_parser_link_google_disabled and self.form_class == DashboardCompanyChangeGoogleForm:
            messages.error(self.request, "Ссылка на филиал в Google сегодня уже обновлялась")

        if self.object.is_parser_link_avito_disabled and self.form_class == DashboardCompanyChangeAvitoForm:
            messages.error(self.request, "Ссылка на филиал в Авито сегодня уже обновлялась")

        if self.object.is_parser_link_zoon_disabled and self.form_class == DashboardCompanyChangeZoonForm:
            messages.error(self.request, "Ссылка на филиал в Zoon сегодня уже обновлялась")

        if self.object.is_parser_link_flamp_disabled and self.form_class == DashboardCompanyChangeFlampForm:
            messages.error(self.request, "Ссылка на филиал в Flamp сегодня уже обновлялась")

        if self.object.is_parser_link_yell_disabled and self.form_class == DashboardCompanyChangeYellForm:
            messages.error(self.request, "Ссылка на филиал в Yell сегодня уже обновлялась")

        if self.object.is_parser_link_prodoctorov_disabled and self.form_class == DashboardCompanyChangeProdoctorovForm:
            messages.error(self.request, "Ссылка на филиал в Продокторов сегодня уже обновлялась")

        if self.object.is_parser_link_yandex_services_disabled and self.form_class == DashboardCompanyChangeYandexServicesForm:
            messages.error(self.request, "Ссылка на филиал в Яндекс Услуги сегодня уже обновлялась")

        if self.object.is_parser_link_otzovik_disabled and self.form_class == DashboardCompanyChangeOtzovikForm:
            messages.error(self.request, "Ссылка на филиал в Otzovik сегодня уже обновлялась")

        if self.object.is_parser_link_irecommend_disabled and self.form_class == DashboardCompanyChangeIrecommendForm:
            messages.error(self.request, "Ссылка на филиал в Irecommend сегодня уже обновлялась")

        if self.object.is_parser_link_tripadvisor_disabled and self.form_class == DashboardCompanyChangeTripadvisorForm:
            messages.error(self.request, "Ссылка на филиал в Tripadvisor сегодня уже обновлялась")

        context["company_list_short"] = company_list_short(self.request.user, self.object.id)
        context["nav"] = "statistic"
        return context

    def get_queryset(self):
        return super().get_queryset().filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_detail", kwargs={"pk": self.kwargs["pk"]})


class CompanyUpdateLinkYandexView(CompanyUpdateView):
    form_class = DashboardCompanyChangeYandexForm
    template_name = "dashboard/company_update_link_yandex.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_yandex:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkGisView(CompanyUpdateView):
    form_class = DashboardCompanyChangeGisForm
    template_name = "dashboard/company_update_link_gis.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_gis:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkGoogleView(CompanyUpdateView):
    form_class = DashboardCompanyChangeGoogleForm
    template_name = "dashboard/company_update_link_google.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_google:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkAvitoView(CompanyUpdateView):
    form_class = DashboardCompanyChangeAvitoForm
    template_name = "dashboard/company_update_link_avito.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_avito:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkZoonView(CompanyUpdateView):
    form_class = DashboardCompanyChangeZoonForm
    template_name = "dashboard/company_update_link_zoon.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_zoon:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkFlampView(CompanyUpdateView):
    form_class = DashboardCompanyChangeFlampForm
    template_name = "dashboard/company_update_link_flamp.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_flamp:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkYellView(CompanyUpdateView):
    form_class = DashboardCompanyChangeYellForm
    template_name = "dashboard/company_update_link_yell.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_yell:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkProdoctorovView(CompanyUpdateView):
    form_class = DashboardCompanyChangeProdoctorovForm
    template_name = "dashboard/company_update_link_prodoctorov.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_prodoctorov:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkYandexServicesView(CompanyUpdateView):
    form_class = DashboardCompanyChangeYandexServicesForm
    template_name = "dashboard/company_update_link_yandex_services.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_yandex_services:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkOtzovikView(CompanyUpdateView):
    form_class = DashboardCompanyChangeOtzovikForm
    template_name = "dashboard/company_update_link_otzovik.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_otzovik:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkIrecommendView(CompanyUpdateView):
    form_class = DashboardCompanyChangeIrecommendForm
    template_name = "dashboard/company_update_link_irecommend.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_irecommend:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateLinkTripadvisorView(CompanyUpdateView):
    form_class = DashboardCompanyChangeTripadvisorForm
    template_name = "dashboard/company_update_link_tripadvisor.html"

    def dispatch(self, *args, **kwargs):
        if not args[0].user.profile.can_parse_tripadvisor:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)


class CompanyUpdateWidgetView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = DashboardCompanyChangeVisibleForm
    model = Company
    success_message = "Виджет успешно обновлен"
    template_name = "dashboard/company_update_widget.html"

    def dispatch(self, *args, **kwargs):
        if not self.get_object().is_active:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_list_short"] = company_list_short(self.request.user, self.object.id)
        context["layout"] = self.request.GET.get("layout", "s"),
        context["nav"] = "widget"
        context["reviews"] = Review.objects.filter(company_id=self.kwargs["pk"], is_visible=True).order_by("-created_at")[:15]
        context["theme"] = self.request.GET.get("theme", "l")
        return context

    def get_queryset(self):
        return super().get_queryset().filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("company_update_widget", kwargs={"pk": self.kwargs["pk"]})


class MasterCompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = DashboardCompanyCreationForm
    model = Company
    template_name = "dashboard/master_company_create.html"
    success_message = "Филиал успешно добавлен"

    def dispatch(self, *args, **kwargs):
        profile = args[0].user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        parsers_chain = []

        """ Инициализация ссылок из API """
        if self.request.COOKIES.get("id_yandex", False):
            form.instance.parser_link_yandex = unquote(f"https://yandex.ru/maps/org/{self.request.COOKIES['name_yandex']}/{self.request.COOKIES['id_yandex']}/reviews")
            form.instance.parser_last_change_at_yandex = datetime.now(timezone.utc)
            form.instance.feedback_link_yandex = unquote(f"https://yandex.ru/maps/org/{self.request.COOKIES['name_yandex']}/{self.request.COOKIES['id_yandex']}/reviews?add-review=true")

        if self.request.COOKIES.get("id_gis", False):
            form.instance.parser_link_gis = unquote(f"https://2gis.ru/firm/{self.request.COOKIES['id_gis']}/tab/reviews")
            form.instance.parser_last_change_at_gis = datetime.now(timezone.utc)
            form.instance.feedback_link_gis = unquote(f"https://2gis.ru/firm/{self.request.COOKIES['id_gis']}/tab/reviews/addreview")

        if self.request.COOKIES.get("id_google", False):
            form.instance.parser_link_google = unquote(f"https://google.com/maps/search/?api=1&query=~&query_place_id={self.request.COOKIES['id_google']}")
            form.instance.parser_last_change_at_google = datetime.now(timezone.utc)
            form.instance.feedback_link_google = unquote(f"https://search.google.com/local/writereview?placeid={self.request.COOKIES['id_google']}")

        """ Сохранение обьекта филиала """
        form_valid = super().form_valid(form)
        form.instance.users.add(self.request.user)

        """ Инициализация и сохранение флага владельца филиала """
        self.request.user.membership_set.filter(company=self.object).update(is_owner=True)

        """ Инициализация и сохранение первичного баланса """
        # profile = self.request.user.profile
        # profile.balance = Money(60, "RUB")
        # profile.save()

        if form.instance.parser_link_yandex:
            parsers_chain.append(parse_yandex_task.s(company_id=form.instance.id))

        if form.instance.parser_link_gis:
            parsers_chain.append(parse_gis_task.s(company_id=form.instance.id))

        if form.instance.parser_link_google:
            parsers_chain.append(parse_google_task.s(company_id=form.instance.id))

        chain(* parsers_chain).apply_async()
        return form_valid

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["card_list"] = []

        if self.request.COOKIES.get("id_yandex", None):
            context["card_list"].append({
                "address": unquote(self.request.COOKIES.get("address_yandex", "")),
                "phone": unquote(self.request.COOKIES.get("phone_yandex", "")),
                "name": unquote(self.request.COOKIES.get("name_yandex", "")),
                "service": Service.YANDEX
            })

        if self.request.COOKIES.get("id_gis", None):
            context["card_list"].append({
                "address": unquote(self.request.COOKIES.get("address_gis", "")),
                "name": unquote(self.request.COOKIES.get("name_gis", "")),
                "service": Service.GIS
            })

        if self.request.COOKIES.get("id_google", None):
            context["card_list"].append({
                "address": unquote(self.request.COOKIES.get("address_google", "")),
                "name": unquote(self.request.COOKIES.get("name_google", "")),
                "service": Service.GOOGLE
            })

        context["nav"] = "master"
        context["sub_nav"] = "data"
        return context

    def get_success_url(self):
        return reverse("company_detail", kwargs={"pk": self.object.id})


class MasterSearchGisView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        card_list = []

        if "query" in request.GET:
            form = DashboardSearchForm(request.GET)

            if form.is_valid():
                card_list = SearchGis.search(form.cleaned_data.get("query"))
        else:
            form = DashboardSearchForm()

        return render(
            request,
            "dashboard/master_search_gis.html", {
                "card_list": card_list,
                "form": form,
                "nav": "master",
                "sub_nav": "gis",
            }
        )


class MasterSearchGoogleView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        card_list = []

        if "query" in request.GET:
            form = DashboardSearchForm(request.GET)

            if form.is_valid():
                card_list = SearchGoogle.search(form.cleaned_data.get("query"))

        else:
            form = DashboardSearchForm()

        return render(
            request,
            "dashboard/master_search_google.html", {
                "card_list": card_list,
                "form": form,
                "nav": "master",
                "sub_nav": "google"
            }
        )


class MasterSearchYandexView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile

        if not profile.is_active or not profile.can_create_company:
            return redirect("profile_update_finance")

        card_list = []

        if "query" in request.GET:
            form = DashboardSearchForm(request.GET)

            if form.is_valid():
                card_list = SearchYandex.search(form.cleaned_data.get("query"))
        else:
            form = DashboardSearchForm()

        return render(
            request,
            "dashboard/master_search_yandex.html",
            {
                "card_list": card_list,
                "form": form,
                "nav": "master",
                "sub_nav": "yandex"
            }
        )


class MembershipUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "company"
    form_class = DashboardMembershipChangeFormSet
    model = Company
    template_name = "dashboard/membership_update.html"
    success_message = "Настройки успешно обновлены"

    def dispatch(self, *args, **kwargs):
        if not self.get_object().is_active:
            return redirect("profile_update_finance")

        return super().dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(self.form_class)
        form.queryset = form.queryset.filter(user=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_list_short"] = company_list_short(self.request.user, self.object.id)
        context["nav"] = "notifications"
        return context

    def get_queryset(self):
        return super().get_queryset().filter(users__in=[self.request.user])

    def get_success_url(self):
        return reverse("membership_update", kwargs={"pk": self.kwargs["pk"]})


class MessageListView(LoginRequiredMixin, FilterView):
    context_object_name = "message_list"
    filterset_class = MessageFilter
    model = Message
    paginate_by = 30
    template_name = "dashboard/message_list.html"

    def dispatch(self, *args, **kwargs):
        __super__ = super().dispatch(*args, **kwargs)

        company = self.get_context_data()["company"]
        if not company.is_active:
            return redirect("profile_update_finance")

        return __super__

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])
        context["company_list_short"] = company_list_short(self.request.user, self.kwargs["company_pk"])
        context["nav"] = "messages"
        return context

    def get_ordering(self):
        return "-created_at"

    def get_queryset(self):
        return super().get_queryset().filter(
            company__in=[self.kwargs["company_pk"]],
            company__users__in=[self.request.user]
        ).select_related("visit_stamp")


class PasswordUpdateView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = DashboardPasswordChangeForm
    template_name = "dashboard/password_update.html"
    success_message = "Профиль успешно обновлен"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["nav"] = "user"
        context["sub_nav"] = "security"
        return context

    def get_success_url(self):
        return reverse("password_update")


class ProfilePayView(LoginRequiredMixin, View):
    def post(self, request):
        period = self.request.POST.get("period", "annually")
        rate = self.request.POST.get("rate", "START")

        if rate in ["START", "REGULAR"] and period in ["annually", "monthly"]:
            amount = request.user.profile.__getattribute__(f"{rate.lower()}_price_{period}_sale")
            payment = Payment.objects.create(amount=Money(amount, "RUB"), period=period.upper(), rate=rate, user=request.user)

            order = Tbank().init_order(payment.api_secret, amount, request.user.email)
            return redirect(order.get("PaymentURL"))


class ProfileCreateBusinessRequest(LoginRequiredMixin, View):
    template_name = "dashboard/profile_create_business_request.html"
    context = {"nav": "finance"}

    def get(self, request):
        form = DashboardBusinessRequestCreationForm()
        return render(request, self.template_name, {"form": form, ** self.context})

    def post(self, request):
        form = DashboardBusinessRequestCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо, ваш запрос успешно отправлен, скоро с вами свяжется наш менеджер")
            return redirect("profile_update_finance")

        return render(request, self.template_name, {"form": form, ** self.context})


class ProfileUpdateFinanceView(LoginRequiredMixin, View):
    template_name = "dashboard/profile_update_finance.html"
    context = {"nav": "finance"}

    def get(self, request):
        period = self.request.GET.get("period", "annually")
        pay_error_code = self.request.GET.get("ErrorCode", None)
        pay_amount = self.request.GET.get("Amount", None)

        if (pay_error_code and int(pay_error_code) == 0) and (pay_amount and int(pay_amount) > 0):
            messages.success(
                request,
                f"Оплата прошла успешно. На баланс профиля зачислено {Money(int(pay_amount) / 100, 'RUB')}"
            )

        elif (pay_error_code and int(pay_error_code) == 1051) and (pay_amount and int(pay_amount) > 0):
            messages.success(
                request,
                f"Оплата не прошла. На баланс профиля не зачислено {Money(int(pay_amount) / 100, 'RUB')}"
            )

        form = DashboardProfileChangeRateForm(request.POST, instance=request.user.profile)
        return render(request, self.template_name, {"form": form, "period": period, ** self.context})

    def post(self, request):
        period = self.request.GET.get("period", "annually")
        form = DashboardProfileChangeRateForm(request.POST, instance=request.user.profile)
        companies_count = Company.objects.filter(users__in=[self.request.user], membership__is_owner=True).count()

        if form['rate'].value() == "START" and companies_count > 1:
            messages.success(request, "Переход на тариф Старт невозможен. Профиль является владельцем более чем 1 филиала")

        elif form['rate'].value() == "REGULAR" and companies_count > 3:
            messages.success(request, "Переход на тариф Стандарт невозможен. Профиль является владельцем более чем 3 филиалов")

        elif form.is_valid():
            form.save()
            messages.success(request, "Тариф успешно обновлен")

        return render(request, self.template_name, {"form": form, "period": period, ** self.context})


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "dashboard/profile_update.html"
    context = {"nav": "user", "sub_nav": "settings"}

    def get(self, request):
        form = DashboardProfileChangeForm(instance=request.user.profile)
        return render(request, self.template_name, {"form": form, **self.context})

    def post(self, request):
        form = DashboardProfileChangeForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен")

        return render(request, self.template_name, {"form": form, **self.context})


class ReviewListView(LoginRequiredMixin, FilterView):
    context_object_name = "review_list"
    filterset_class = ReviewFilter
    paginate_by = 30
    model = Review
    template_name = "dashboard/review_list.html"

    def dispatch(self, *args, **kwargs):
        __super__ = super().dispatch(*args, **kwargs)

        company = self.get_context_data()["company"]
        if not company.is_active:
            return redirect("profile_update_finance")

        return __super__

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])
        context["company_list_short"] = company_list_short(self.request.user, self.kwargs["company_pk"])
        context["nav"] = "reviews"
        return context

    def get_ordering(self):
        return ["-created_at", "service", "stars"]

    def get_queryset(self):
        return super().get_queryset().filter(
            company__in=[self.kwargs.get("company_pk")],
            company__users__in=[self.request.user]
        )


class ReviewUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = "review"
    form_class = DashboardReviewChangeForm
    model = Review
    success_message = "Отзыв успешно обновлен"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["company_pk"], users__in=[self.request.user])
        return context

    def get_queryset(self):
        return super().get_queryset().filter(company__in=[self.kwargs["company_pk"]], company__users__in=[self.request.user])

    def get_success_url(self):
        return f"{reverse('review_list', kwargs={'company_pk': self.kwargs['company_pk']})}?{self.request.GET.urlencode()}"


class StoryUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        story.users.add(request.user)
        return JsonResponse({})


class UserCreateView(FormView):
    form_class = DashboardUserCreationForm
    template_name = "dashboard/user_create.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["nav"] = "registration"
        return context

    def get_success_url(self):
        return reverse("company_list")


class UserLoginView(LoginView):
    form_class = DashboardAuthenticationForm
    template_name = "dashboard/user_login.html"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context["nav"] = "login"
        return context


class UserLogoutView(LoginRequiredMixin, LogoutView):
    ...


class UserUpdateView(LoginRequiredMixin, View):
    template_name = "dashboard/user_update.html"
    context = {"nav": "user", "sub_nav": "account"}

    def get(self, request):
        form = DashboardUserChangeForm(instance=request.user)
        return render(request, self.template_name, {"form": form, **self.context})

    def post(self, request):
        form = DashboardUserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен")

        return render(request, self.template_name, {"form": form, **self.context})
