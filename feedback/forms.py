from django import forms

from resources.models import NegativeMessage


class NegativeMessageForm(forms.ModelForm):

    phone = forms.CharField(
        label=False,
        max_length=100
    )

    text = forms.CharField(
        label=False,
        max_length=500,
        required=False,
        widget=forms.Textarea
    )

    class Meta:
        model = NegativeMessage
        fields = ["phone", "text"]

    # Конструктор формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Поле тегов
        # self.fields["negative_message_tag"].widget.attrs["class"] = "tag_widget"

        # Поле комментарий
        self.fields["text"].widget.attrs["class"] = "bp5-input bp5-fill"
        self.fields["text"].widget.attrs["placeholder"] = "Расскажите подробнее, но достаточно и отмеченных тегов"
        self.fields["text"].widget.attrs["rows"] = 4

        # Поле телефон
        self.fields["phone"].widget.attrs["class"] = "bp5-input bp5-fill"
        self.fields["phone"].widget.attrs["placeholder"] = "+7"
