from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Website

def website_detail(request, path):
    website = get_object_or_404(Website, path = path)
    return render(request, 'website/detail.html', {'website': website})