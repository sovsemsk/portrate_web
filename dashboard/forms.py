from django.contrib.auth.forms import (
    AuthenticationForm,
    SetPasswordForm,
    UserChangeForm,
    UsernameField,
    UserCreationForm
)
from django.contrib.auth.models import User
from django.forms import BooleanField, ImageField, Select, inlineformset_factory
from django.forms import CharField, PasswordInput, ModelForm, TextInput
from django.forms.widgets import FileInput

from resources.models import Company, Profile, Review, Timezone, Membership


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["default_timezone"]

    default_timezone = Select(choices=Timezone.choices)


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["address", "phone", "logo", "name"]

    address = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    phone = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    logo = ImageField(widget=FileInput(), required=False)
    name = CharField(widget=TextInput(attrs={"class": "bp5-input"}))


class CompanyParserForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "parser_link_yandex",
            "is_parse_yandex",
            "parser_link_gis",
            "is_parse_gis",
            "parser_link_google",
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

    parser_link_yandex = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    is_parse_yandex = BooleanField(required=False)
    parser_link_gis = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    is_parse_gis = BooleanField(required=False)
    parser_link_google = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    is_parse_google = BooleanField(required=False)


class CompanyDataForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "address",
            "phone",
            "logo",
            "name"
        ]

    address = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    phone = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    logo = ImageField(widget=FileInput(), required=False)
    name = CharField(widget=TextInput(attrs={"class": "bp5-input"}))


class CompanyLinkForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "form_link_yandex",
            "form_link_gis",
            "form_link_google",
            "form_link_dikidi",
            "form_link_restoclub",
            "form_link_tripadvisor",
            "form_link_prodoctorov",
            "form_link_flamp",
            "form_link_zoon",
            "form_link_otzovik",
            "form_link_irecommend"
        ]

    form_link_yandex = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_gis = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_google = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_dikidi = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_restoclub = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_tripadvisor = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_prodoctorov = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_flamp = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_zoon = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_otzovik = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_link_irecommend = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)


class CompanyContactForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "form_contact_whatsapp",
            "form_contact_telegram",
            "form_contact_viber",
            "form_contact_website",
            "form_contact_vk",
            "form_contact_ok",
            "form_contact_facebook",
            "form_contact_instagram",
            "form_contact_youtube",
            "form_contact_x",
        ]

    form_contact_whatsapp = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_contact_telegram = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_contact_viber = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_contact_website = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_contact_vk = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_contact_ok = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_contact_facebook = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_contact_instagram = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_contact_youtube = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)
    form_contact_x = CharField(widget=TextInput(attrs={"class": "bp5-input"}), required=False)


class CompanyMembershipForm(ModelForm):
    class Meta:
        model = Membership

        fields = [
            "can_notify_negative_portrate",
            "can_notify_negative_yandex",
            "can_notify_negative_gis",
            "can_notify_negative_google"
        ]

        can_notify_negative_portrate = BooleanField(required=False)
        can_notify_negative_yandex = BooleanField(required=False)
        can_notify_negative_gis = BooleanField(required=False)
        can_notify_negative_google = BooleanField(required=False)

CompanyMembershipFormSet = inlineformset_factory(
    Company,
    Membership,
    can_delete=False,
    extra=0,
    form=CompanyMembershipForm
)


class ReviewForm(ModelForm):
    is_hidden = BooleanField(required=False)

    class Meta:
        model = Review
        fields = ["is_visible"]


class DashboardUserCreationForm(UserCreationForm):
    username = UsernameField(widget=TextInput(attrs={"class": "bp5-input"}))
    password1 = CharField(widget=PasswordInput(attrs={"class": "bp5-input"}))
    password2 = CharField(widget=PasswordInput(attrs={"class": "bp5-input"}))


class DashboardAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=TextInput(attrs={"class": "bp5-input"}))
    password = CharField(widget=PasswordInput(attrs={"class": "bp5-input"}))

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