from django.forms import DateInput, ModelForm, Select, TimeField, widgets, BooleanField, CharField, ImageField

from extensions.models import Profile, Timezone
from resources.models import Company, Review


class DateInput(DateInput):
    input_type = "date"


class ProfileForm(ModelForm):
    default_timezone = Select(choices=Timezone.choices)
    can_notify_at_start = TimeField(widget=widgets.TimeInput(attrs={"type": "time", "class": "bp5-input"}))
    can_notify_at_end = TimeField(widget=widgets.TimeInput(attrs={"type": "time", "class": "bp5-input"}))
    can_notify_negative_portrate = BooleanField(required=False)
    can_notify_negative_yandex = BooleanField(required=False)
    can_notify_negative_gis = BooleanField(required=False)
    can_notify_negative_google = BooleanField(required=False)

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


class CompanyForm(ModelForm):
    address = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}))
    logo = ImageField(widget=widgets.FileInput(), required=False)
    name = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}))

    parser_link_yandex = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    parser_link_gis = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    parser_link_google = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)

    form_link_yandex = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_gis = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_google = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_mapsme = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_dikidi = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_restoclub = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_tripadvisor = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_prodoctorov = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_flamp = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_zoon = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_otzovik = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_irecommend = CharField(widget=widgets.TextInput(attrs={"class": "bp5-input"}), required=False)

    is_parse_yandex = BooleanField(required=False)
    is_parse_gis = BooleanField(required=False)
    is_parse_google = BooleanField(required=False)

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


class ReviewForm(ModelForm):
    is_hidden = BooleanField(required=False)

    class Meta:
        model = Review
        fields = ["is_visible"]
