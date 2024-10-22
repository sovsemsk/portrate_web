from datetime import datetime, timezone

from celery import chain
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.forms import (
    CharField,
    CheckboxSelectMultiple,
    EmailField,
    ModelForm,
    MultipleChoiceField,
    NumberInput,
    PasswordInput,
    TextInput,
    Textarea
)

from django.forms import Form, inlineformset_factory, Select, ImageField, FileInput, BooleanField, CheckboxInput

from resources.models import Company, Membership, Profile, Rate, Review, Service, Timezone
from resources.tasks import (
    parse_yandex_task,
    parse_gis_task,
    parse_google_task,
    parse_avito_task,
    parse_zoon_task,
    parse_flamp_task,
    parse_yell_task,
    parse_prodoctorov_task,
    parse_yandex_services_task,
    parse_otzovik_task,
    parse_irecommend_task,
    parse_tripadvisor_task
)

class SwitchSelectMultiple(CheckboxSelectMultiple):
    option_template_name = "forms/widgets/switch_option.html"

class DashboardAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Пользователь не найден",
        "inactive": "Аккаунт не активен"
    }

    username = UsernameField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))
    password = CharField(widget=PasswordInput(attrs={"class": "bp5-input bp5-large"}))


class DashboardBusinessRequestCreationForm(Form):
    name = CharField(label="Имя", widget=TextInput(attrs={"class": "bp5-input bp5-large", "autofocus": ""}))
    phone = CharField(label="Телефон", widget=TextInput(attrs={"class": "bp5-input bp5-large", "data-phone": ""}))
    company_name = CharField(label="Название компании", widget=TextInput(attrs={"class": "bp5-input bp5-large"}))
    companies_count = CharField(label="Количество филиалов", widget=NumberInput(attrs={"class": "bp5-input bp5-large"}))
    services = MultipleChoiceField(choices=Service.choices, label="Сервисы", widget=SwitchSelectMultiple)

    def save(self):
        send_mail(
            f"Заявка на бизнес тариф от {self.cleaned_data.get('name')}, {self.cleaned_data.get('phone')}",
            f"""Имя - {self.cleaned_data.get('name')}
Телефон - {self.cleaned_data.get('phone')}
Название компании - {self.cleaned_data.get('company_name')}
Количество филиалов - {self.cleaned_data.get('companies_count')}
Сервисы - {", ".join(self.cleaned_data.get('services'))}
""",
            "noreply@portrate.io",
            ["sovsemsk@gmail.com", "sakiruma@gmail.com", "service@portrate.io"]
        )


class DashboardCompanyChangeYandexForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_yandex"]

    parser_link_yandex = CharField(
        required=False,
        # validators=[RegexValidator(
        #     regex=r"^https:\/\/yandex\.ru\/maps\/org\/[\w\W]{1,}\/[\d]{1,}\/reviews[\/]{0,1}$",
        #     message="Введите правильную ссылку «https://yandex.ru/maps/org/{NAME}/{ID}/reviews/»",
        #     code="invalid_parser_link_yandex",
        # )],
        widget=TextInput(attrs={"class": "bp5-input bp5-large"}),
    )

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_yandex"].disabled = self.instance.is_parser_link_yandex_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_yandex_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.YANDEX).delete()
            self.instance.is_first_parsing_yandex = True
            self.instance.parser_last_change_at_yandex = datetime.now(timezone.utc)
            self.instance.rating_yandex = 0.0

            """ Перезапуск парсера """
            parse_yandex_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeGisForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_gis"]

    parser_link_gis = CharField(
        required=False,
        # validators=[RegexValidator(
        #     regex=r"^https:\/\/2gis\.ru\/firm\/[\d]{1,}\/tab\/reviews[\/]{0,1}$",
        #     message="Введите правильную ссылку «https://2gis.ru/firm/{ID}/tab/reviews»",
        #     code="invalid_parser_link_yandex",
        # )],
        widget=TextInput(attrs={"class": "bp5-input bp5-large"}),
    )

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_gis"].disabled = self.instance.is_parser_link_gis_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_gis_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.GIS).delete()
            self.instance.is_first_parsing_gis = True
            self.instance.parser_last_change_at_gis = datetime.now(timezone.utc)
            self.instance.rating_gis = 0.0

            """ Перезапуск парсера """
            parse_gis_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeGoogleForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_google"]

    parser_link_google = CharField(
        required=False,
        # validators=[RegexValidator(
        #     regex=r"^https:\/\/google\.com\/maps\/search\/\?api=1&query=~&query_place_id=[\w\W]{1,}[\/]{0,1}$",
        #     message="Введите правильную ссылку «https://google.com/maps/search/?api=1&query=~&query_place_id={ID}»",
        #     code="invalid_parser_link_yandex",
        # )],
        widget=TextInput(attrs={"class": "bp5-input bp5-large"}),
    )

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_google"].disabled = self.instance.is_parser_link_google_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_google_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.GOOGLE).delete()
            self.instance.is_first_parsing_google = True
            self.instance.parser_last_change_at_google = datetime.now(timezone.utc)
            self.instance.rating_google = 0.0

            """ Перезапуск парсера """
            parse_google_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeAvitoForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_avito"]

    parser_link_avito = CharField(
        required=False,
        # validators=[RegexValidator(
        #     regex=r"^https:\/\/avito\.ru\/brands\/[\w\W]{1,}\/$",
        #     message="Введите правильную ссылку «https://avito.ru/brands/{NAME}/»",
        #     code="invalid_parser_link_yandex",
        # )],
        widget=TextInput(attrs={"class": "bp5-input bp5-large"})
    )

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_avito"].disabled = self.instance.is_parser_link_avito_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_avito_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.AVITO).delete()
            self.instance.is_first_parsing_avito = True
            self.instance.parser_last_change_at_avito = datetime.now(timezone.utc)
            self.instance.rating_avito = 0.0

            """ Перезапуск парсера """
            parse_avito_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeZoonForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_zoon"]

    # https://zoon.ru/msk/medical/klinika_lichnyj_doktor_na_ulitse_novatorov/

    parser_link_zoon = CharField(
        required=False,
        # validators=[RegexValidator(
        #     regex=r"^https:\/\/zoon\.ru\/[\w\W]{1,}\/[\w\W]{1,}\/[\w\W]{1,}\/$",
        #     message="Введите правильную ссылку «https://zoon.ru/{CITY}/{CATEGORY}/{NAME}/»",
        #     code="invalid_parser_link_yandex",
        # )],
        widget=TextInput(attrs={"class": "bp5-input bp5-large"})
    )

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_zoon"].disabled = self.instance.is_parser_link_zoon_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_zoon_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.ZOON).delete()
            self.instance.is_first_parsing_zoon = True
            self.instance.parser_last_change_at_zoon = datetime.now(timezone.utc)
            self.instance.rating_zoon = 0.0

            """ Перезапуск парсера """
            parse_zoon_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeFlampForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_flamp"]

    parser_link_flamp = CharField(required=False, widget=TextInput(attrs={"class": "bp5-input bp5-large"}))

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_flamp"].disabled = self.instance.is_parser_link_flamp_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_flamp_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.FLAMP).delete()
            self.instance.is_first_parsing_flamp = True
            self.instance.parser_last_change_at_flamp = datetime.now(timezone.utc)
            self.instance.rating_flamp = 0.0

            """ Перезапуск парсера """
            parse_flamp_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeYellForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_yell"]

    parser_link_yell = CharField(required=False, widget=TextInput(attrs={"class": "bp5-input bp5-large"}))

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_yell"].disabled = self.instance.is_parser_link_yell_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_yell_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.YELL).delete()
            self.instance.is_first_parsing_yell = True
            self.instance.parser_last_change_at_yell = datetime.now(timezone.utc)
            self.instance.rating_yell = 0.0

            """ Перезапуск парсера """
            parse_yell_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeProdoctorovForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_prodoctorov"]

    parser_link_prodoctorov = CharField(required=False, widget=TextInput(attrs={"class": "bp5-input bp5-large"}))

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_prodoctorov"].disabled = self.instance.is_parser_link_prodoctorov_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_prodoctorov_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.PRODOCTOROV).delete()
            self.instance.is_first_parsing_prodoctorov = True
            self.instance.parser_last_change_at_prodoctorov = datetime.now(timezone.utc)
            self.instance.rating_prodoctorov = 0.0

            """ Перезапуск парсера """
            parse_prodoctorov_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeYandexServicesForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_yandex_services"]

    parser_link_yandex_services = CharField(required=False, widget=TextInput(attrs={"class": "bp5-input bp5-large"}))

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_yandex_services"].disabled = self.instance.is_parser_link_yandex_services_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_yandex_services_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.YANDEX_SERVICES).delete()
            self.instance.is_first_parsing_yandex_services = True
            self.instance.parser_last_change_at_yandex_services = datetime.now(timezone.utc)
            self.instance.rating_yandex_services = 0.0

            """ Перезапуск парсера """
            parse_yandex_services_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeOtzovikForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_otzovik"]

    parser_link_otzovik = CharField(required=False, widget=TextInput(attrs={"class": "bp5-input bp5-large"}))

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_otzovik"].disabled = self.instance.is_parser_link_otzovik_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_otzovik_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.OTZOVIK).delete()
            self.instance.is_first_parsing_otzovik = True
            self.instance.parser_last_change_at_otzovik = datetime.now(timezone.utc)
            self.instance.rating_otzovik = 0.0

            """ Перезапуск парсера """
            parse_otzovik_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeIrecommendForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_irecommend"]

    parser_link_irecommend = CharField(required=False, widget=TextInput(attrs={"class": "bp5-input bp5-large"}))

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_irecommend"].disabled = self.instance.is_parser_link_irecommend_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_irecommend_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.IRECOMMEND).delete()
            self.instance.is_first_parsing_irecommend = True
            self.instance.parser_last_change_at_irecommend = datetime.now(timezone.utc)
            self.instance.rating_irecommend = 0.0

            """ Перезапуск парсера """
            parse_irecommend_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyChangeDataForm(ModelForm):
    class Meta:
        model = Company
        fields = ["address", "logo", "name", "phone"]

    address = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    logo = ImageField(widget=FileInput(attrs={"accept": "image/png, image/jpeg", "data-file": ""}), required=False)
    name = CharField(widget=TextInput(attrs={"class": "bp5-input  bp5-large"}))
    phone = CharField(widget=TextInput(attrs={"class": "bp5-input  bp5-large", "data-phone": ""}), required=False)


class DashboardCompanyChangeContactForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "feedback_contact_whatsapp",
            "feedback_contact_telegram",
            "feedback_contact_viber",
            "feedback_contact_website",
            "feedback_contact_vk",
            "feedback_contact_ok",
            "feedback_contact_facebook",
            "feedback_contact_instagram",
            "feedback_contact_x",
            "feedback_contact_youtube",
            "feedback_contact_rutube",
            "feedback_contact_vimeo"
        ]

    feedback_contact_whatsapp = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_telegram = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_viber = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_website = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_vk = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_ok = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_facebook = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_instagram = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_x = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_youtube = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_rutube = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_contact_vimeo = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)


class DashboardCompanyChangeTextForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "feedback_text_rate_heading",
            "feedback_text_request_heading",
            "feedback_text_create_heading",
            "feedback_text_success_heading",
            "feedback_text_success_text"
        ]

    feedback_text_rate_heading = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))
    feedback_text_request_heading = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))
    feedback_text_create_heading = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))
    feedback_text_success_heading = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))
    feedback_text_success_text = CharField(widget=Textarea(attrs={"class": "bp5-input bp5-large"}))


class DashboardCompanyChangeServiceForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "feedback_link_yandex",
            "feedback_link_gis",
            "feedback_link_google",
            "feedback_link_avito",
            "feedback_link_zoon",
            "feedback_link_flamp",
            "feedback_link_yell",
            "feedback_link_prodoctorov",
            "feedback_link_yandex_services",
            "feedback_link_otzovik",
            "feedback_link_irecommend",
            "feedback_link_tripadvisor",
        ]

    feedback_link_yandex = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_gis = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_google = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_avito = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_zoon = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_flamp = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_yell = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_prodoctorov = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_yandex_services = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_otzovik = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_irecommend = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)
    feedback_link_tripadvisor = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}), required=False)


class DashboardCompanyChangeVisibleForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "is_visible_0",
            "is_visible_1",
            "is_visible_2",
            "is_visible_3",
            "is_visible_4",
            "is_visible_5",
            "is_visible_portrate",
            "is_visible_yandex",
            "is_visible_gis",
            "is_visible_google",
            "is_visible_avito",
            "is_visible_zoon",
            "is_visible_flamp",
            "is_visible_yell",
            "is_visible_prodoctorov",
            "is_visible_yandex_services",
            "is_visible_otzovik",
            "is_visible_irecommend",
            "is_visible_tripadvisor",
            "is_visible_short"
        ]

    is_visible_0 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_1 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_2 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_3 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_4 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_5 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_portrate = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_yandex = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_gis = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_google = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_avito = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_zoon = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_flamp = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_yell = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_prodoctorov = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_yandex_services = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_otzovik = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_irecommend = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_visible_tripadvisor = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)

    def is_valid(self):
        is_valid = super().is_valid()

        for stars in range(6):
            for service in Service:
                self.instance.review_set.filter(
                    is_moderated=False,
                    stars=stars,
                    service=service
                ).update(
                    is_visible=self.instance.__getattribute__(f"is_visible_{stars}") and self.instance.__getattribute__(f"is_visible_{service.lower()}")
                )

        return is_valid


class DashboardCompanyChangeTripadvisorForm(ModelForm):
    class Meta:
        model = Company
        fields = ["parser_link_tripadvisor"]

    parser_link_tripadvisor = CharField(required=False, widget=TextInput(attrs={"class": "bp5-input bp5-large"}))

    def __init__(self, *args, **kwargs):
        __init__ = super().__init__(*args, **kwargs)
        self.fields["parser_link_tripadvisor"].disabled = self.instance.is_parser_link_tripadvisor_disabled
        return __init__

    def is_valid(self):
        is_valid = super().is_valid()

        if self.instance.is_parser_run_tripadvisor_need:
            """ Очистка прошлых данных """
            self.instance.review_set.filter(service=Service.TRIPADVISOR).delete()
            self.instance.is_first_parsing_tripadvisor = True
            self.instance.parser_last_change_at_tripadvisor = datetime.now(timezone.utc)
            self.instance.rating_tripadvisor = 0.0

            """ Перезапуск парсера """
            parse_tripadvisor_task.delay(company_id=self.instance.id)

        return is_valid


class DashboardCompanyCreationForm(ModelForm):
    class Meta:
        model = Company
        fields = ["address", "logo", "name", "phone"]

    address = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large", "data-address": ""}), required=False)
    logo = ImageField(widget=FileInput(attrs={"accept": "image/png, image/jpeg", "data-file": ""}), required=False)
    name = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large", "data-name": ""}))
    phone = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large", "data-phone": ""}), required=False)

    def save(self):
        save = super().save()
        parsers_chain = []

        if self.instance.parser_link_yandex:
            parsers_chain.append(parse_yandex_task.s(company_id=self.instance.id))

        if self.instance.parser_link_gis:
            parsers_chain.append(parse_gis_task.s(company_id=self.instance.id))

        if self.instance.parser_link_google:
            parsers_chain.append(parse_google_task.s(company_id=self.instance.id))

        chain(* parsers_chain).apply_async()
        return save


class DashboardCompanyCreationLinkYandexForm(Form):
    parser_link_yandex = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))


class DashboardCompanyCreationLinkGisForm(Form):
    parser_link_gis = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))


class DashboardCompanyCreationLinkGoogleForm(Form):
    parser_link_google = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))


class DashboardMembershipChangeForm(ModelForm):
    class Meta:
        model = Membership

        fields = [
            "is_notify_0",
            "is_notify_1",
            "is_notify_2",
            "is_notify_3",
            "is_notify_4",
            "is_notify_5",
            "is_notify_portrate",
            "is_notify_yandex",
            "is_notify_gis",
            "is_notify_google",
            "is_notify_avito",
            "is_notify_zoon",
            "is_notify_flamp",
            "is_notify_yell",
            "is_notify_prodoctorov",
            "is_notify_yandex_services",
            "is_notify_otzovik",
            "is_notify_irecommend",
            "is_notify_tripadvisor"
        ]

    is_notify_0 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_1 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_2 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_3 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_4 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_5 = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_portrate = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_yandex = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_gis = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_google = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_avito = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_zoon = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_flamp = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_yell = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_prodoctorov = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_yandex_services = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_otzovik = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_irecommend = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)
    is_notify_tripadvisor = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)


DashboardMembershipChangeFormSet = inlineformset_factory(
    Company,
    Membership,
    can_delete=False,
    extra=0,
    form=DashboardMembershipChangeForm
)


class DashboardProfileChangeForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["default_timezone"]

    default_timezone = Select(choices=Timezone.choices)


class DashboardProfileChangeRateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["rate"]

    default_timezone = Select(choices=Rate.choices)


class DashboardReviewChangeForm(ModelForm):
    class Meta:
        model = Review
        fields = ["is_moderated", "is_visible"]

    is_visible = BooleanField(widget=CheckboxInput(attrs={"data-input": ""}), required=False)

    def is_valid(self):
        is_valid = super().is_valid()
        self.instance.is_moderated = True
        return is_valid


class DashboardSearchForm(Form):
    query = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large", "autofocus": ""}))


class DashboardPasswordChangeForm(PasswordChangeForm):
    old_password = CharField(strip=False, widget=PasswordInput(attrs={"autocomplete": "new-password", "class": "bp5-input bp5-large"}))
    new_password1 = CharField(strip=False, widget=PasswordInput(attrs={"autocomplete": "new-password", "class": "bp5-input bp5-large"}))
    new_password2 = CharField(strip=False, widget=PasswordInput(attrs={"autocomplete": "new-password", "class": "bp5-input bp5-large"}))


class DashboardUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "username"]

    email = CharField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))
    username = UsernameField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))


class DashboardUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    username = UsernameField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))
    email = EmailField(widget=TextInput(attrs={"class": "bp5-input bp5-large"}))
    password1 = CharField(widget=PasswordInput(attrs={"class": "bp5-input bp5-large"}))
    password2 = CharField(widget=PasswordInput(attrs={"class": "bp5-input bp5-large"}))

