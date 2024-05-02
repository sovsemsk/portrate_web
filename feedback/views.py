from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from feedback.forms import MessageForm
from resources.models import Company, Message


@require_http_methods(["GET"])
def rate(request, company_pk):
    company = get_object_or_404(Company, id=company_pk)
    return render(request, "feedback/rate.html", {"company": company})


@require_http_methods(["GET", "POST"])
def create(request, company_pk):
    company = get_object_or_404(Company, id=company_pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        form.instance.company = company

        if form.is_valid():
            form.save()
            company.messages_total_count = Message.objects.filter(company_id=company.id).count()
            company.save()
            return redirect(reverse("success", kwargs={"company_pk": company.id}))

    else:
        form = MessageForm()

    return render(request, "feedback/create.html", {"company": company, "form": form})


@require_http_methods(["GET"])
def request(request, company_pk):
    company = get_object_or_404(Company, id=company_pk)
    return render(request, "feedback/request.html", {"company": company})


@require_http_methods(["GET"])
def success(request, company_pk):
    company = get_object_or_404(Company, id=company_pk)
    return render(request, "feedback/success.html", {"company": company})
