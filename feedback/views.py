from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from resources.models import Website
from .models import NegativeMessageTag, NegativeMessage
from .forms import NegativeMessageForm


def rate(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render(request, 'feedback/rate.html', {'website': website})


def create(request, website_id):
    website = get_object_or_404(Website, id=website_id)

    if request.method == 'POST':
        form = NegativeMessageForm(request.POST)

        if form.is_valid():
            # @TODO: Перенести добавление группы в форму и сохранять через форму
            negative_message = NegativeMessage(
                group_id=website.group.id, branch_id=website.branch.id, phone=form['phone'].value(), text=form['text'].value()
            )
            negative_message.save()
            return redirect(f'/~{website_id}')
    else:
        form = NegativeMessageForm()
        return render(request, 'feedback/create.html', {'website': website, 'form': form})


def request(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render(request, 'feedback/request.html', {'website': website})
