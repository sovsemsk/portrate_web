from django.shortcuts import render
from django.shortcuts import get_object_or_404
from resources.models import Website


def rate(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render(request, 'feedback/rate.html', {'website': website})


def create(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render(request, 'feedback/create.html', {'website': website})


def request(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render(request, 'feedback/request.html', {'website': website})
