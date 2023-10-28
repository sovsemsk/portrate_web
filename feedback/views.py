from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from resources.models import Company, Notification
from feedback.forms import NegativeMessageForm


@require_http_methods(['GET'])
def rate(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    return render(request, 'feedback/rate.html', {'company': company})


@require_http_methods(['GET', 'POST'])
def create(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        form = NegativeMessageForm(request.POST)
        form.instance.company = company

        if form.is_valid():
            negative_message = form.save()

            Notification.objects.create(
                company=negative_message.company,
                negative_message=negative_message,
                text=negative_message.text,
            )

            return redirect(f'/~{company_id}')

    else:
        form = NegativeMessageForm()

    return render(request, 'feedback/create.html', {'company': company, 'form': form})


@require_http_methods(['GET'])
def request(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    return render(request, 'feedback/request.html', {'company': company})
