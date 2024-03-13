from django import forms

from resources.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["phone", "text"]

    phone = forms.CharField(label=False, max_length=100)
    text = forms.CharField(label=False, max_length=500, required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["class"] = "bp5-input bp5-fill"
        self.fields["text"].widget.attrs["placeholder"] = "Расскажите подробнее, но достаточно и отмеченных тегов"
        self.fields["text"].widget.attrs["rows"] = 4
        self.fields["phone"].widget.attrs["class"] = "bp5-input bp5-fill"
        self.fields["phone"].widget.attrs["placeholder"] = "+7"
