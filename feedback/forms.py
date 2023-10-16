from django import forms
from .models import NegativeMessageTag


class NegativeMessageForm(forms.Form):
    phone = forms.CharField(label="Номер телефона", max_length=100)
    text = forms.CharField(label="Текст сообщения", max_length=500)
    negative_message_tags = forms.ModelMultipleChoiceField(
        queryset=NegativeMessageTag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
