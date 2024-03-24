from django.forms import ModelForm, Textarea, CharField, TextInput

from resources.models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["phone", "text"]

    phone = CharField(label=False, max_length=100, widget=TextInput(attrs={"class": "bp5-input bp5-fill bp5-large", "placeholder": "+7"}))
    text = CharField(label=False, max_length=500, required=False, widget=Textarea(attrs={"class": "bp5-input bp5-fill pio-input", "rows": 4}))
