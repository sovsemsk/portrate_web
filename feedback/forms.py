from django import forms
from .models import NegativeMessage, NegativeMessageTag


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

    negative_message_tag = forms.ModelMultipleChoiceField(
        label=False,
        queryset=NegativeMessageTag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = NegativeMessage
        fields = ['phone', 'text', 'negative_message_tag']

    # Конструктор формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Поле тегов
        self.fields['negative_message_tag'].widget.attrs['class'] = 'tag_widget'

        # Поле комментарий
        self.fields['text'].widget.attrs['class'] = 'text_area_widget'
        self.fields['text'].widget.attrs['placeholder'] = 'Расскажите подробнее, но достаточно и отмеченных тегов'
        self.fields['text'].widget.attrs['rows'] = 4

        # Поле телефон
        self.fields['phone'].widget.attrs['class'] = 'char_field_widget'
        self.fields['phone'].widget.attrs['placeholder'] = '+7'
