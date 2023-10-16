from django.shortcuts import render
from django.shortcuts import get_object_or_404
from resources.models import Website
from .models import NegativeMessageTag
from .forms import NegativeMessageForm


def rate(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render(request, 'feedback/rate.html', {'website': website})


def create(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    tags = NegativeMessageTag.objects.all()

    if request.method == 'POST':
        form = NegativeMessageForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = NegativeMessageForm()
    return render(request, 'feedback/create.html', {'website': website, 'tags': tags, 'form': form})


def request(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render(request, 'feedback/request.html', {'website': website})
