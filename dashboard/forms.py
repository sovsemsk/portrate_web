from django import forms
from extensions.models import Profile


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    default_timezone = forms.Select(
        choices=Profile.DefaultTimezone.choices
    )

    can_notify_at_start = forms.TimeField(widget=forms.widgets.TimeInput(
        attrs={'type': 'time', 'class': 'bp5-input w-36'}
    ))

    can_notify_at_end = forms.TimeField(widget=forms.widgets.TimeInput(
        attrs={'type': 'time', 'class': 'bp5-input w-36'}
    ))

    can_notify_negative_portrate = forms.BooleanField(required=False)
    can_notify_negative_yandex = forms.BooleanField(required=False)
    can_notify_negative_gis = forms.BooleanField(required=False)
    can_notify_negative_google = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = [
            'default_timezone',
            'can_notify_at_start',
            'can_notify_at_end',
            'can_notify_negative_portrate',
            'can_notify_negative_yandex',
            'can_notify_negative_gis',
            'can_notify_negative_google'
        ]

    # Конструктор формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
