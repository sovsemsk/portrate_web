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
    logo = forms.CharField(
        widget=forms.widgets.FileInput(),
        required=False
    )

    name = forms.CharField(widget=forms.widgets.TextInput(
        attrs={'class': 'bp5-input max-w-sm'}
    ))

    address = forms.CharField(widget=forms.widgets.TextInput(
        attrs={'class': 'bp5-input max-w-sm'}
    ))

    yandex_id = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    gis_id = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    google_id = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'bp5-input max-w-sm'}),
        required=False
    )

    mapsme_id = forms.CharField(
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

            'yandex_id',
            'is_yandex_reviews_upload',
            'is_yandex_reviews_download',

            'gis_id',
            'is_gis_reviews_upload',
            'is_gis_reviews_download',

            'google_id',
            'is_google_reviews_upload',
            'is_google_reviews_download',

            'mapsme_id',
            'is_mapsme_reviews_upload',
            'is_mapsme_reviews_download',

            # 'dikidi_id',
            # 'is_dikidi_reviews_upload',
            # 'is_dikidi_reviews_upload',

            # 'restoclub_id',
            # 'is_mapsme_reviews_upload',
            # 'is_mapsme_reviews_upload',

            # 'tripadvisor_id',
            # 'is_tripadvisor_reviews_upload',
            # 'is_tripadvisor_reviews_upload',

            # 'prodoctorov_id',
            # 'is_prodoctorov_reviews_upload',
            # 'is_prodoctorov_reviews_upload',

            # 'flamp_id',
            # 'is_flamp_reviews_upload',
            # 'is_flamp_reviews_upload',

            # 'zoon_id',
            # 'is_zoon_reviews_upload',
            # 'is_zoon_reviews_upload',

            # 'otzovik_id',
            # 'is_otzovik_reviews_upload',
            # 'is_otzovik_reviews_upload',

            # 'irecommend_id',
            # 'is_irecommend_reviews_upload',
            # 'is_irecommend_reviews_upload',

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
