from django.shortcuts import render
from django.shortcuts import get_object_or_404
from resources.models import Website


def website_detail(request, path):
    website = get_object_or_404(Website, path=path)
    return render(request, 'resources/website_detail.html', {'website': website})
