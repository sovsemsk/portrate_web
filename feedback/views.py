from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from feedback.forms import ClickStampForm, MessageForm
from resources.models import Company, VisitStamp


def create_session(func):
    """ Создание сессии для анонимных пользователей """

    def decorator(request, *args, **kwargs):
        if not request.session or not request.session.session_key:
            request.session.save()

        try:
            VisitStamp.objects.create(
                id=request.session.session_key,
                company_id=kwargs.get("company_pk", None),
                utm_source=request.GET.get("utm_source", "Прямой")
            )
        except:
            ...

        return func(request, *args, **kwargs)

    return decorator


@require_http_methods(["GET"])
@create_session
def rate(request, company_pk):
    company = get_object_or_404(Company, id=company_pk)
    return render(request, "feedback/rate.html", {"company": company})


@require_http_methods(["GET", "POST"])
@create_session
def create(request, company_pk):
    company = get_object_or_404(Company, id=company_pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        form.instance.company = company
        form.instance.visit_stamp_id = request.session.session_key

        if form.is_valid():
            form.save()
            return redirect(reverse("success", kwargs={"company_pk": company.id}))

    else:
        form = MessageForm()

    return render(request, "feedback/create.html", {"company": company, "form": form})


@require_http_methods(["GET", "POST"])
@create_session
def request(request, company_pk):
    company = get_object_or_404(Company, id=company_pk)

    if request.method == "POST":
        form = ClickStampForm(request.POST)
        form.instance.company_id = company_pk
        form.instance.visit_stamp_id = request.session.session_key

        if form.is_valid():
            form.save()
            return redirect(company.__getattribute__(f"feedback_link_{form.instance.service.lower()}"))

    return render(request, "feedback/request.html", {"company": company })


@require_http_methods(["GET"])
@create_session
def success(request, company_pk):
    company = get_object_or_404(Company, id=company_pk)
    return render(request, "feedback/success.html", {"company": company})
