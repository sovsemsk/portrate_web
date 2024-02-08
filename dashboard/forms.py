from django import forms

from extensions.models import Profile
from resources.models import Company


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
    can_notify_negative_mapsme = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = [
            'default_timezone',
            'can_notify_at_start',
            'can_notify_at_end',
            'can_notify_negative_portrate',
            'can_notify_negative_yandex',
            'can_notify_negative_gis',
            'can_notify_negative_google',
            'can_notify_negative_mapsme'
        ]

    # Конструктор формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CompanyForm(forms.ModelForm):
    # ID
    logo = forms.ImageField(
        widget=forms.widgets.FileInput(),
        required=False
    )

    name = forms.CharField(widget=forms.widgets.TextInput(
        attrs={'class': 'bp5-input max-w-sm'}
    ))

    address = forms.CharField(widget=forms.widgets.TextInput(
        attrs={'class': 'bp5-input max-w-sm'}
    ))

    yandex_parser_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    gis_parser_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    google_parser_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    # Ссылки
    yandex_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    gis_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    google_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    mapsme_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    dikidi_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    restoclub_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    tripadvisor_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    prodoctorov_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    zoon_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    otzovik_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    irecommend_link = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    # Парсеры
    is_yandex_reviews_upload = forms.BooleanField(required=False)
    is_yandex_reviews_download = forms.BooleanField(required=False)
    is_gis_reviews_upload = forms.BooleanField(required=False)
    is_gis_reviews_download = forms.BooleanField(required=False)
    is_google_reviews_upload = forms.BooleanField(required=False)
    is_google_reviews_download = forms.BooleanField(required=False)
    is_mapsme_reviews_upload = forms.BooleanField(required=False)
    is_mapsme_reviews_upload = forms.BooleanField(required=False)

    class Meta:
        model = Company
        fields = [
            'logo',
            'name',
            'address',

            'yandex_parser_link',
            'is_yandex_reviews_upload',
            'is_yandex_reviews_download',

            'gis_parser_link',
            'is_gis_reviews_upload',
            'is_gis_reviews_download',

            'google_parser_link',
            'is_google_reviews_upload',
            'is_google_reviews_download',

            'yandex_link',
            'gis_link',
            'google_link',
            'mapsme_link',
            'dikidi_link',
            'restoclub_link',
            'tripadvisor_link',
            'prodoctorov_link',
            'zoon_link',
            'otzovik_link',
            'irecommend_link',
        ]

    # Конструктор формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
