from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from resources.models import Notification, Website
from feedback.forms import NegativeMessageForm



@require_http_methods(['GET'])
def rate(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render(request, 'feedback/rate.html', {'website': website})


@require_http_methods(['GET', 'POST'])
def create(request, website_id):
    website = get_object_or_404(Website, id=website_id)

    if request.method == 'POST':
        form = NegativeMessageForm(request.POST)

        if form.is_valid():
            form.instance.company = website.company
            form.instance.branch = website.branch
            negative_message = form.save()
            
            Notification.objects.create(
                company=negative_message.company,
                negative_message=negative_message,
                text=negative_message.text,
            )

            return redirect(f'/~{website_id}')

    else:
        form = NegativeMessageForm()

    return render(request, 'feedback/create.html', {'website': website, 'form': form})


@require_http_methods(['GET'])
def request(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render(request, 'feedback/request.html', {'website': website})
