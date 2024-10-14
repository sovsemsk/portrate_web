from django.forms import HiddenInput, ModelForm, Textarea, CharField, TextInput, ChoiceField

from resources.models import ClickStamp, Message, Service


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["phone", "text"]

    phone = CharField(
        label=False,
        max_length=100,
        widget=TextInput(
            attrs={
                "class": "bp5-input bp5-fill bp5-large",
                "data-phone": "", "placeholder": "+7"
            }
        )
    )

    text = CharField(
        label=False,
        max_length=500,
        required=False,
        widget=Textarea(
            attrs={
                "class": "bp5-input bp5-fill pio-input",
                "data-textarea": "",
                "rows": 4
            }
        ))



class ClickStampForm(ModelForm):
    class Meta:
        model = ClickStamp
        fields = ["service"]

    service = ChoiceField(widget=HiddenInput(), choices=[(service.name, service.value) for service in Service])
