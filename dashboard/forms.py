from django import forms

from extensions.models import Profile, Timezone
from resources.models import Company, Review


class DateInput(forms.DateInput):
    input_type = "date"


class ProfileForm(forms.ModelForm):
    default_timezone = forms.Select(choices=Timezone.choices)
    can_notify_at_start = forms.TimeField(widget=forms.widgets.TimeInput(attrs={"type": "time", "class": "bp5-input"}))
    can_notify_at_end = forms.TimeField(widget=forms.widgets.TimeInput(attrs={"type": "time", "class": "bp5-input"}))
    can_notify_negative_portrate = forms.BooleanField(required=False)
    can_notify_negative_yandex = forms.BooleanField(required=False)
    can_notify_negative_gis = forms.BooleanField(required=False)
    can_notify_negative_google = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = [
            "default_timezone",
            "can_notify_at_start",
            "can_notify_at_end",
            "can_notify_negative_portrate",
            "can_notify_negative_yandex",
            "can_notify_negative_gis",
            "can_notify_negative_google"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CompanyForm(forms.ModelForm):
    address = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}))
    logo = forms.ImageField(widget=forms.widgets.FileInput(), required=False)
    name = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}))

    parser_link_yandex = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    parser_link_gis = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    parser_link_google = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)

    form_link_yandex = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_gis = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_google = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_mapsme = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_dikidi = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_restoclub = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_tripadvisor = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_prodoctorov = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_flamp = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_zoon = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_otzovik = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_irecommend = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "bp5-input"}), required=False)

    is_parse_yandex = forms.BooleanField(required=False)
    is_parse_gis = forms.BooleanField(required=False)
    is_parse_google = forms.BooleanField(required=False)

    class Meta:
        model = Company
        fields = [
            "address",
            "logo",
            "name",

            "parser_link_yandex",
            "parser_link_gis",
            "parser_link_google",

            "form_link_yandex",
            "form_link_gis",
            "form_link_google",
            "form_link_mapsme",
            "form_link_dikidi",
            "form_link_restoclub",
            "form_link_tripadvisor",
            "form_link_prodoctorov",
            "form_link_flamp",
            "form_link_zoon",
            "form_link_otzovik",
            "form_link_irecommend",

            "is_parse_yandex",
            "is_parse_gis",
            "is_parse_google"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.data and self.data.get("is_parse_yandex"):
                self.fields.get("parser_link_yandex").required = True

        if self.data and self.data.get("is_parse_gis"):
                self.fields.get("parser_link_gis").required = True

        if self.data and self.data.get("is_parse_google"):
                self.fields.get("parser_link_google").required = True


class ReviewForm(forms.ModelForm):
    is_hidden = forms.BooleanField(required=False)

    class Meta:
        model = Review
        fields = ["is_hidden"]
