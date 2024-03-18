from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, UsernameField, SetPasswordForm
from django.contrib.auth.models import User
from django.forms import BooleanField, ImageField, Select, TimeField
from django.forms import CharField, PasswordInput, ModelForm, TextInput
from django.forms.widgets import TimeInput, FileInput

from resources.models import Company, Profile, Review, Timezone


class ProfileForm(ModelForm):
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

    default_timezone = Select(choices=Timezone.choices)
    can_notify_at_start = TimeField(widget=TimeInput(attrs={"type": "time", "class": "bp5-input"}))
    can_notify_at_end = TimeField(widget=TimeInput(attrs={"type": "time", "class": "bp5-input"}))
    can_notify_negative_portrate = BooleanField(required=False)
    can_notify_negative_yandex = BooleanField(required=False)
    can_notify_negative_gis = BooleanField(required=False)
    can_notify_negative_google = BooleanField(required=False)


class CompanyForm(ModelForm):
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

    address = CharField(widget=TextInput(attrs={"class": "bp5-input"}))
    logo = ImageField(widget=FileInput(), required=False)
    name = CharField(widget=TextInput(attrs={"class": "bp5-input"}))

    parser_link_yandex = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    parser_link_gis = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    parser_link_google = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)

    form_link_yandex = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_gis = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_google = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_mapsme = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_dikidi = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_restoclub = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_tripadvisor = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_prodoctorov = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_flamp = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_zoon = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_otzovik = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_irecommend = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)

    is_parse_yandex = BooleanField(required=False)
    is_parse_gis = BooleanField(required=False)
    is_parse_google = BooleanField(required=False)


class ReviewForm(ModelForm):
    is_hidden = BooleanField(required=False)

    class Meta:
        model = Review
        fields = ["is_visible"]


class DashboardAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=TextInput(attrs={"class": "bp5-input", "placeholder": "Логин"}))
    password = CharField(widget=PasswordInput(attrs={"class": "bp5-input", "placeholder": "Пароль"}))

    error_messages = {
        "invalid_login": "Пользователь не найден",
        "inactive": "Аккаунт не активен"
    }


class DashboardUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]

    email = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    first_name = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    last_name = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    username = UsernameField(widget=TextInput(attrs={"class": "bp5-input"}))


class DashboardSetPasswordForm(SetPasswordForm):
    new_password1 = CharField(widget=PasswordInput(attrs={"class": "bp5-input", "autocomplete": "new-password"}), strip=False)
    new_password2 = CharField(strip=False,widget=PasswordInput(attrs={"class": "bp5-input", "autocomplete": "new-password"}))