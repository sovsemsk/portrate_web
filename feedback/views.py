from django.db import IntegrityError
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from feedback.forms import ClickStampForm, MessageForm
from resources.models import Company, VisitStamp, Membership, Profile


def create_session(func):
    """ Создание сессии для анонимных пользователей """

    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session.save()

            try:
                VisitStamp.objects.create(
                    id=request.session.session_key,
                    company_id=kwargs.get("pk", None),
                    utm_source=request.GET.get("utm_source", "Прямой")
                )
            except IntegrityError:
                ...

        return func(request, *args, **kwargs)

    return decorator


@require_http_methods(["GET"])
@create_session
def rate(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, "feedback/rate.html", {"company": company})


@require_http_methods(["GET", "POST"])
@create_session
def create(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        form.instance.company = company
        form.instance.visit_stamp_id = request.session.session_key

        if form.is_valid():
            form.save()
            return redirect(reverse("success", kwargs={"pk": company.id}))

    else:
        form = MessageForm()

    return render(request, "feedback/create.html", {"company": company, "form": form})


@require_http_methods(["GET", "POST"])
@create_session
def request(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":
        form = ClickStampForm(request.POST)
        form.instance.company_id = pk
        form.instance.visit_stamp_id = request.session.session_key

        if not request.user.is_authenticated and form.is_valid():
            form.save()

        return redirect(company.__getattribute__(f"feedback_link_{form.instance.service.lower()}"))

    return render(request, "feedback/request.html", {"company": company })


@require_http_methods(["GET"])
@create_session
def success(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, "feedback/success.html", {"company": company})
